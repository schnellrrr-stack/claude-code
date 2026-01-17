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
        criteria: Optional[Dict[str, Any]] = None,
        company_sizes: Optional[List[str]] = None,
        industries: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 25
    ) -> Dict[str, Any]:
        """
        Search for organizations using Apollo.io API.

        Args:
            criteria: Dict with search criteria (new interface)
            company_sizes: List of company size ranges (legacy)
            industries: List of industries (legacy)
            locations: List of locations (legacy)
            page: Page number for pagination
            per_page: Number of results per page (max 100)

        Returns:
            API response with organization data
        """
        endpoint = f"{self.BASE_URL}/organizations/search"

        # Handle new criteria-based interface
        if criteria is not None:
            company_sizes = criteria.get("company_size", [])
            industries = criteria.get("industries", [])
            locations = criteria.get("locations", [])
        else:
            # Use defaults from config if not provided (legacy interface)
            if company_sizes is None:
                company_sizes = settings.get_company_sizes_list()
            if industries is None:
                industries = settings.get_industries_list()
            if locations is None:
                locations = []

        payload = {
            "page": page,
            "per_page": min(per_page, 100)
        }

        # Add optional fields if provided
        if company_sizes:
            payload["organization_num_employees_ranges"] = company_sizes
        if industries:
            payload["q_organization_keyword_tags"] = industries
        if locations:
            payload["organization_locations"] = locations

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

    def format_companies(self, raw_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Format raw Apollo organization API results into a clean company list.

        Args:
            raw_results: Raw API response from Apollo

        Returns:
            List of formatted company dictionaries
        """
        if not raw_results or raw_results.get("error"):
            return []

        organizations = raw_results.get("organizations", [])
        formatted_companies = []

        for org in organizations:
            company = {
                "name": org.get("name", ""),
                "website": org.get("website_url", ""),
                "linkedin_url": org.get("linkedin_url", ""),
                "twitter_url": org.get("twitter_url", ""),
                "facebook_url": org.get("facebook_url", ""),
                "phone": org.get("phone", ""),
                "industry": org.get("industry", ""),
                "industries": org.get("industries", []),
                "keywords": org.get("keywords", []),
                "estimated_num_employees": org.get("estimated_num_employees", ""),
                "city": org.get("city", ""),
                "state": org.get("state", ""),
                "country": org.get("country", ""),
                "postal_code": org.get("postal_code", ""),
                "street_address": org.get("street_address", ""),
                "founded_year": org.get("founded_year", ""),
                "publicly_traded_symbol": org.get("publicly_traded_symbol", ""),
                "revenue": org.get("organization_revenue_printed", ""),
            }

            formatted_companies.append(company)

        return formatted_companies
