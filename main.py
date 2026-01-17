"""Main lead generation system."""
import json
import sys
from typing import Optional, List
from apollo_connector import ApolloConnector
from config import settings


class LeadGenerator:
    """Lead generation system using Apollo.io."""

    def __init__(self):
        """Initialize lead generator."""
        self.apollo = ApolloConnector()

    def generate_leads(
        self,
        person_titles: Optional[List[str]] = None,
        company_sizes: Optional[List[str]] = None,
        industries: Optional[List[str]] = None,
        max_results: Optional[int] = None
    ) -> List[dict]:
        """
        Generate leads based on search criteria.

        Args:
            person_titles: List of job titles to search for
            company_sizes: List of company size ranges
            industries: List of industries
            max_results: Maximum number of results to retrieve

        Returns:
            List of lead dictionaries
        """
        max_results = max_results or settings.max_results
        per_page = min(max_results, 100)
        all_leads = []

        print(f"Searching for leads with criteria:")
        print(f"  Titles: {person_titles or settings.get_person_titles_list()}")
        print(f"  Company Sizes: {company_sizes or settings.get_company_sizes_list()}")
        print(f"  Industries: {industries or settings.get_industries_list()}")
        print(f"  Max Results: {max_results}\n")

        page = 1
        while len(all_leads) < max_results:
            print(f"Fetching page {page}...")

            result = self.apollo.search_people(
                person_titles=person_titles,
                company_sizes=company_sizes,
                industries=industries,
                page=page,
                per_page=per_page
            )

            if result.get("error"):
                print(f"Error: {result.get('message')}")
                break

            people = result.get("people", [])
            if not people:
                print("No more results found.")
                break

            # Extract relevant lead information
            for person in people:
                lead = self._extract_lead_info(person)
                all_leads.append(lead)

                if len(all_leads) >= max_results:
                    break

            print(f"Retrieved {len(people)} leads (Total: {len(all_leads)})")

            # Check if there are more pages
            pagination = result.get("pagination", {})
            if page >= pagination.get("total_pages", 1):
                break

            page += 1

        print(f"\nTotal leads generated: {len(all_leads)}")
        return all_leads

    def _extract_lead_info(self, person: dict) -> dict:
        """
        Extract relevant information from Apollo person object.

        Args:
            person: Person data from Apollo API

        Returns:
            Simplified lead dictionary
        """
        organization = person.get("organization", {}) or {}

        return {
            "name": person.get("name"),
            "title": person.get("title"),
            "email": person.get("email"),
            "linkedin_url": person.get("linkedin_url"),
            "phone": person.get("phone_numbers", [{}])[0].get("raw_number") if person.get("phone_numbers") else None,
            "company": {
                "name": organization.get("name"),
                "website": organization.get("website_url"),
                "industry": organization.get("industry"),
                "size": organization.get("estimated_num_employees"),
                "location": organization.get("city"),
            }
        }

    def export_leads(self, leads: List[dict], filename: str = "leads.json"):
        """
        Export leads to a file.

        Args:
            leads: List of lead dictionaries
            filename: Output filename
        """
        with open(filename, "w") as f:
            json.dump(leads, f, indent=2)
        print(f"Leads exported to {filename}")

    def check_api_health(self):
        """Check Apollo API health and credits."""
        print("Checking API health...")
        result = self.apollo.get_credits()

        if result.get("error"):
            print(f"Error: {result.get('message')}")
            return False

        print("API Status: OK")
        print(f"Credits remaining: {result.get('credits_remaining', 'Unknown')}")
        return True


def main():
    """Main entry point for lead generation system."""
    print("=" * 60)
    print("Lead Generation System - Powered by Apollo.io")
    print("=" * 60)
    print()

    # Initialize lead generator
    try:
        generator = LeadGenerator()
    except Exception as e:
        print(f"Error initializing lead generator: {e}")
        print("\nMake sure you have:")
        print("1. Created a .env file with your APOLLO_API_KEY")
        print("2. Installed dependencies: pip install -r requirements.txt")
        sys.exit(1)

    # Check API health
    if not generator.check_api_health():
        print("\nAPI health check failed. Please verify your API key.")
        sys.exit(1)

    print()

    # Generate leads
    leads = generator.generate_leads(
        max_results=10  # Start with 10 leads for testing
    )

    if leads:
        # Export to file
        generator.export_leads(leads, "leads.json")

        # Display sample leads
        print("\n" + "=" * 60)
        print("Sample Leads (first 3):")
        print("=" * 60)
        for i, lead in enumerate(leads[:3], 1):
            print(f"\nLead {i}:")
            print(f"  Name: {lead['name']}")
            print(f"  Title: {lead['title']}")
            print(f"  Email: {lead['email']}")
            print(f"  Company: {lead['company']['name']}")
            print(f"  Industry: {lead['company']['industry']}")
    else:
        print("\nNo leads generated.")


if __name__ == "__main__":
    main()
