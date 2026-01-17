#!/usr/bin/env python
"""Search for EMS (Electronics Manufacturing Services) companies."""
import json
from datetime import datetime
from apollo_connector import ApolloConnector

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

    # Get pagination info
    pagination = raw_results.get("pagination", {})
    total_available = pagination.get('total_entries', 0)
    print(f"   Total available: {total_available:,}")
    print()

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = f"output/ems_companies_{timestamp}.json"

    output_data = {
        "generated_at": datetime.now().isoformat(),
        "search_description": "EMS manufacturing companies with 50-500 employees in United States",
        "criteria_used": criteria,
        "total_companies": len(companies),
        "total_available": total_available,
        "companies": companies
    }

    with open(json_file, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"💾 Results saved to: {json_file}")
    print()

    # Display preview
    print("=" * 60)
    print("📋 COMPANY PREVIEW (First 10)")
    print("=" * 60)

    for i, company in enumerate(companies[:10], 1):
        print(f"\n{i}. {company['name']}")
        if company['industry']:
            print(f"   Industry: {company['industry']}")
        if company['estimated_num_employees']:
            print(f"   Size: {company['estimated_num_employees']:,} employees")
        else:
            print(f"   Size: Unknown")
        location_parts = [company['city'], company['state'], company['country']]
        location = ', '.join([p for p in location_parts if p])
        if location:
            print(f"   Location: {location}")
        if company['website']:
            print(f"   Website: {company['website']}")
        if company['phone']:
            print(f"   Phone: {company['phone']}")
        if company.get('keywords'):
            print(f"   Keywords: {', '.join(company['keywords'][:5])}")

    print()
    print("=" * 60)
    print(f"✅ SEARCH COMPLETED - {len(companies)} companies found")
    print("=" * 60)

    return json_file

if __name__ == "__main__":
    search_ems_companies()
