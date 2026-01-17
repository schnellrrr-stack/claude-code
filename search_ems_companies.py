#!/usr/bin/env python
"""Search for companies based on ICP criteria."""
import json
import csv
import io
import sys
from datetime import datetime
from apollo_connector import ApolloConnector

def filter_by_employee_count(companies, min_emp, max_emp):
    """Filter companies by employee count range."""
    filtered = []
    for company in companies:
        emp_count = company.get('estimated_num_employees', '')
        if not emp_count:
            continue
        try:
            emp_count = int(emp_count)
            if min_emp <= emp_count <= max_emp:
                filtered.append(company)
        except (ValueError, TypeError):
            continue
    return filtered

def companies_to_csv_string(companies):
    """Convert companies list to CSV string."""
    fieldnames = [
        'name', 'website', 'linkedin_url', 'twitter_url', 'facebook_url',
        'phone', 'industry', 'estimated_num_employees', 'city', 'state',
        'country', 'postal_code', 'street_address', 'founded_year',
        'publicly_traded_symbol', 'revenue', 'keywords'
    ]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for company in companies:
        # Handle keywords list
        if company.get('keywords'):
            company['keywords'] = '; '.join(company['keywords'])
        # Write row
        row = {k: company.get(k, '') for k in fieldnames}
        writer.writerow(row)

    return output.getvalue()

def search_companies(
    industries=None,
    min_employees=50,
    max_employees=500,
    locations=None,
    description="Company Search"
):
    """
    Search for companies based on ICP criteria.

    Args:
        industries: List of industry keywords
        min_employees: Minimum employee count
        max_employees: Maximum employee count
        locations: List of locations (countries, states, cities)
        description: Description of the search
    """
    print("=" * 60)
    print(f"🔍 {description.upper()}")
    print("=" * 60)
    print()

    # Initialize Apollo connector
    apollo = ApolloConnector()

    # Map employee ranges to Apollo's format
    company_size_ranges = []
    if min_employees <= 50 and max_employees >= 10:
        company_size_ranges.append("1-10")
    if min_employees <= 50 and max_employees >= 50:
        company_size_ranges.append("11-50")
    if min_employees <= 200 and max_employees >= 51:
        company_size_ranges.append("51-200")
    if min_employees <= 500 and max_employees >= 201:
        company_size_ranges.append("201-500")
    if min_employees <= 1000 and max_employees >= 501:
        company_size_ranges.append("501-1000")
    if min_employees <= 5000 and max_employees >= 1001:
        company_size_ranges.append("1001-5000")
    if max_employees > 5000:
        company_size_ranges.append("5001+")

    # Define search criteria
    criteria = {
        "company_size": company_size_ranges,
        "industries": industries or ["Manufacturing"],
        "locations": locations or ["United States"]
    }

    print("📋 Search Criteria:")
    print(f"   Industries: {', '.join(criteria['industries'])}")
    print(f"   Employee Range: {min_employees}-{max_employees}")
    print(f"   Locations: {', '.join(criteria['locations'])}")
    print(f"   Apollo Size Ranges: {', '.join(criteria['company_size'])}")
    print()

    # Search Apollo for companies
    print("📊 Searching Apollo.io...")
    raw_results = apollo.search_organizations(criteria=criteria, per_page=100)

    if raw_results.get("error"):
        print(f"❌ Error: {raw_results.get('message')}")
        if raw_results.get('status_code'):
            print(f"   Status Code: {raw_results.get('status_code')}")
        return None

    # Format results
    companies = apollo.format_companies(raw_results)
    print(f"✅ Found {len(companies)} companies")

    # Filter by exact employee count range
    filtered_companies = filter_by_employee_count(companies, min_employees, max_employees)
    print(f"✅ Filtered to {len(filtered_companies)} companies ({min_employees}-{max_employees} employees)")

    # Get pagination info
    pagination = raw_results.get("pagination", {})
    total_available = pagination.get('total_entries', 0)
    print(f"   Total available in database: {total_available:,}")
    print()

    # Display preview
    print("=" * 60)
    print("📋 COMPANY PREVIEW (First 10 of filtered results)")
    print("=" * 60)

    for i, company in enumerate(filtered_companies[:10], 1):
        print(f"\n{i}. {company['name']}")
        if company['industry']:
            print(f"   Industry: {company['industry']}")
        if company['estimated_num_employees']:
            print(f"   Employees: {company['estimated_num_employees']:,}")
        location_parts = [company['city'], company['state'], company['country']]
        location = ', '.join([p for p in location_parts if p])
        if location:
            print(f"   Location: {location}")
        if company['website']:
            print(f"   Website: {company['website']}")
        if company['phone']:
            print(f"   Phone: {company['phone']}")

    print()
    print("=" * 60)
    print(f"✅ SEARCH COMPLETED - {len(filtered_companies)} companies ({min_employees}-{max_employees} employees)")
    print("=" * 60)
    print()

    # Ask user if they want CSV export
    export_choice = input("📥 Do you want to export results to CSV? (yes/no): ").strip().lower()

    if export_choice in ['yes', 'y']:
        print()
        print("=" * 60)
        print("📄 CSV OUTPUT (Copy the text below)")
        print("=" * 60)
        print()
        csv_content = companies_to_csv_string(filtered_companies)
        print(csv_content)
        print("=" * 60)
        print(f"✅ CSV data displayed above ({len(filtered_companies)} companies)")
        print("=" * 60)
    else:
        print()
        print("✅ Results not exported to CSV")
        print(f"📊 Summary: Found {len(filtered_companies)} companies with {min_employees}-{max_employees} employees")

    return filtered_companies


if __name__ == "__main__":
    # Default: EMS manufacturing companies with 50-500 employees in United States
    ems_industries = [
        "Electronics",
        "Electronics Manufacturing",
        "Electronic Manufacturing",
        "EMS",
        "Contract Manufacturing",
        "Electrical/Electronic Manufacturing",
        "Manufacturing",
        "PCB Assembly",
        "Circuit Board Manufacturing"
    ]

    search_companies(
        industries=ems_industries,
        min_employees=50,
        max_employees=500,
        locations=["United States"],
        description="EMS Manufacturing Companies Search"
    )
