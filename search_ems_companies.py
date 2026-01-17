#!/usr/bin/env python
"""Search for EMS (Electronics Manufacturing Services) companies."""
import json
import csv
import io
from datetime import datetime
from apollo_connector import ApolloConnector

def filter_by_employee_count(companies, min_emp=50, max_emp=500):
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

def search_ems_companies():
    """Search for EMS manufacturing companies with 50-500 employees in US."""
    print("=" * 60)
    print("🔍 EMS MANUFACTURING COMPANIES SEARCH")
    print("=" * 60)
    print()

    # Initialize Apollo connector
    apollo = ApolloConnector()

    # Define search criteria for EMS companies
    criteria = {
        "company_size": [
            "51-200",      # 51-200 employees
            "201-500"      # 201-500 employees
        ],
        "industries": [
            "Electronics",
            "Electronics Manufacturing",
            "Electronic Manufacturing",
            "EMS",
            "Contract Manufacturing",
            "Electrical/Electronic Manufacturing",
            "Manufacturing",
            "PCB Assembly",
            "Circuit Board Manufacturing"
        ],
        "locations": [
            "United States"
        ]
    }

    print("📋 Search Criteria:")
    print(json.dumps(criteria, indent=2))
    print()

    # Search Apollo for companies
    print("📊 Searching Apollo.io for EMS companies...")
    raw_results = apollo.search_organizations(criteria=criteria, per_page=100)

    if raw_results.get("error"):
        print(f"❌ Error: {raw_results.get('message')}")
        if raw_results.get('status_code'):
            print(f"   Status Code: {raw_results.get('status_code')}")
        return None

    # Format results
    companies = apollo.format_companies(raw_results)
    print(f"✅ Found {len(companies)} companies")

    # Filter by employee count (50-500)
    filtered_companies = filter_by_employee_count(companies, 50, 500)
    print(f"✅ Filtered to {len(filtered_companies)} companies (50-500 employees)")

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
    print(f"✅ SEARCH COMPLETED - {len(filtered_companies)} companies (50-500 employees)")
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
        print(f"📊 Summary: Found {len(filtered_companies)} EMS companies with 50-500 employees")

    return filtered_companies

if __name__ == "__main__":
    search_ems_companies()
