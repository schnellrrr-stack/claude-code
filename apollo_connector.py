"""Apollo.io API connector for lead generation."""
import requests
from typing import Optional, Dict, List, Any
from config import settings


class ApolloConnector:
    """Connector for Apollo.io API interactions."""

    BASE_URL = "https://api.apollo.io/v1"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Apollo connector.

        Args:
            api_key: Apollo.io API key. If not provided, uses config.
        """
        self.api_key = api_key or settings.apollo_api_key
        self.headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": self.api_key
        }

    def search_people(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        person_titles: Optional[List[str]] = None,
        company_sizes: Optional[List[str]] = None,
        industries: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 25
    ) -> Dict[str, Any]:
        """
        Search for people using Apollo.io API.

        Args:
            criteria: Dict with search criteria (new interface)
            person_titles: List of job titles to search for (legacy)
            company_sizes: List of company size ranges (legacy)
            industries: List of industries (legacy)
            page: Page number for pagination
            per_page: Number of results per page (max 100)

        Returns:
            API response with people data
        """
        endpoint = f"{self.BASE_URL}/mixed_people/search"

        # Handle new criteria-based interface
        if criteria is not None:
            person_titles = criteria.get("job_titles", [])
            company_sizes = criteria.get("company_size", [])
            industries = criteria.get("industries", [])
            seniority_levels = criteria.get("seniority_levels", [])
            locations = criteria.get("locations", [])
        else:
            # Use defaults from config if not provided (legacy interface)
            if person_titles is None:
                person_titles = settings.get_person_titles_list()
            if company_sizes is None:
                company_sizes = settings.get_company_sizes_list()
            if industries is None:
                industries = settings.get_industries_list()
            seniority_levels = []
            locations = []

        payload = {
            "person_titles": person_titles,
            "organization_num_employees_ranges": company_sizes,
            "q_organization_keyword_tags": industries,
            "page": page,
            "per_page": min(per_page, 100)  # API max is 100
        }

        # Add optional fields if provided
        if seniority_levels:
            payload["person_seniorities"] = seniority_levels
        if locations:
            payload["person_locations"] = locations

        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"API request failed: {str(e)}",
                "status_code": getattr(e.response, "status_code", None)
            }

    def search_organizations(
        self,
        company_sizes: Optional[List[str]] = None,
        industries: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 25
    ) -> Dict[str, Any]:
        """
        Search for organizations using Apollo.io API.

        Args:
            company_sizes: List of company size ranges
            industries: List of industries
            page: Page number for pagination
            per_page: Number of results per page (max 100)

        Returns:
            API response with organization data
        """
        endpoint = f"{self.BASE_URL}/mixed_companies/search"

        # Use defaults from config if not provided
        if company_sizes is None:
            company_sizes = settings.get_company_sizes_list()
        if industries is None:
            industries = settings.get_industries_list()

        payload = {
            "organization_num_employees_ranges": company_sizes,
            "organization_industry_tag_ids": industries,
            "page": page,
            "per_page": min(per_page, 100)
        }

        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"API request failed: {str(e)}",
                "status_code": getattr(e.response, "status_code", None)
            }

    def enrich_person(self, email: str) -> Dict[str, Any]:
        """
        Enrich person data by email.

        Args:
            email: Email address to enrich

        Returns:
            API response with enriched person data
        """
        endpoint = f"{self.BASE_URL}/people/match"

        payload = {"email": email}

        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"API request failed: {str(e)}",
                "status_code": getattr(e.response, "status_code", None)
            }

    def get_credits(self) -> Dict[str, Any]:
        """
        Get current API credit usage.

        Returns:
            API response with credit information
        """
        endpoint = f"{self.BASE_URL}/auth/health"

        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"API request failed: {str(e)}",
                "status_code": getattr(e.response, "status_code", None)
            }

    def format_leads(self, raw_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Format raw Apollo API results into a clean lead list.

        Args:
            raw_results: Raw API response from Apollo

        Returns:
            List of formatted lead dictionaries
        """
        if not raw_results or raw_results.get("error"):
            return []

        people = raw_results.get("people", [])
        formatted_leads = []

        for person in people:
            organization = person.get("organization", {}) or {}

            lead = {
                "first_name": person.get("first_name", ""),
                "last_name": person.get("last_name", ""),
                "name": person.get("name", ""),
                "title": person.get("title", ""),
                "email": person.get("email", ""),
                "linkedin_url": person.get("linkedin_url", ""),
                "phone": person.get("phone_numbers", [{}])[0].get("raw_number", "") if person.get("phone_numbers") else "",
                "company_name": organization.get("name", ""),
                "company_website": organization.get("website_url", ""),
                "company_industry": organization.get("industry", ""),
                "company_size": organization.get("estimated_num_employees", ""),
                "company_location": organization.get("city", ""),
            }

            formatted_leads.append(lead)

        return formatted_leads
