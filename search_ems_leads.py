#!/usr/bin/env python
"""Search for EMS (Electronics Manufacturing Services) leads."""
import json
from datetime import datetime
from apollo_connector import ApolloConnector

def search_ems_leads():
    """Search for EMS manufacturing companies in the United States."""
    print("=" * 60)
    print("🔍 EMS MANUFACTURING LEADS GENERATION")
    print("=" * 60)
    print()

    # Initialize Apollo connector
    apollo = ApolloConnector()

    # Define search criteria for EMS manufacturing companies
    # 50-500 employees = "51-200" and "201-500" ranges
    criteria = {
        "company_size": [
            "51-200",
            "201-500"
        ],
        "industries": [
            "Electronics Manufacturing",
            "Contract Manufacturing",
            "EMS",
            "Electronics",
            "Manufacturing",
            "PCB Assembly",
            "Electronic Components",
            "Electrical/Electronic Manufacturing"
        ],
        "locations": [
            "United States"
        ]
    }

    print("📋 Search Criteria:")
    print(f"   Industry: EMS (Electronics Manufacturing Services)")
    print(f"   Employee Count: 50-500")
    print(f"   Location: United States")
    print()
    print("Detailed criteria:")
    print(json.dumps(criteria, indent=2))
    print()

    # Search Apollo for companies
    print("📊 Searching Apollo.io for EMS companies...")
    raw_results = apollo.search_organizations(criteria=criteria, per_page=100)

    if raw_results.get("error"):
        print(f"❌ Error: {raw_results.get('message')}")
        if raw_results.get('status_code'):
            print(f"   Status Code: {raw_results.get('status_code')}")
        return

    # Format results
    companies = apollo.format_companies(raw_results)
    print(f"✅ Found {len(companies)} companies")

    # Get pagination info
    pagination = raw_results.get("pagination", {})
    total_available = pagination.get('total_entries', 0)
    print(f"   Total available in Apollo: {total_available:,}")
    print()

    # Save results to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = f"output/ems_leads_{timestamp}.json"

    output_data = {
        "generated_at": datetime.now().isoformat(),
        "search_description": "EMS manufacturing companies, 50-500 employees, United States",
        "criteria_used": criteria,
        "total_companies": len(companies),
        "total_available": total_available,
        "companies": companies
    }

    with open(json_file, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"💾 JSON results saved to: {json_file}")
    print()

    # Convert to CSV
    print("📄 Converting to CSV format...")
    from convert_to_csv import json_to_csv
    csv_file = json_to_csv(json_file)
    print(f"✅ CSV results saved to: {csv_file}")
    print()

    # Display preview
    print("=" * 60)
    print("📋 COMPANY PREVIEW (First 10)")
    print("=" * 60)

    for i, company in enumerate(companies[:10], 1):
        print(f"\n{i}. {company['name']}")
        print(f"   Industry: {company['industry']}")
        if company['estimated_num_employees']:
            print(f"   Size: {company['estimated_num_employees']:,} employees")
        else:
            print(f"   Size: Unknown")

        location_parts = []
        if company['city']:
            location_parts.append(company['city'])
        if company['state']:
            location_parts.append(company['state'])
        if company['country']:
            location_parts.append(company['country'])
        print(f"   Location: {', '.join(location_parts)}")

        if company['website']:
            print(f"   Website: {company['website']}")
        if company['phone']:
            print(f"   Phone: {company['phone']}")
        if company['founded_year']:
            print(f"   Founded: {company['founded_year']}")
        if company['revenue']:
            print(f"   Revenue: {company['revenue']}")
        if company.get('keywords'):
            print(f"   Keywords: {', '.join(company['keywords'][:5])}")

    print()
    print("=" * 60)
    print("✅ EMS LEADS GENERATION COMPLETED")
    print("=" * 60)
    print()
    print(f"📊 Summary:")
    print(f"   Companies retrieved: {len(companies)}")
    print(f"   Total available: {total_available:,}")
    print(f"   JSON file: {json_file}")
    print(f"   CSV file: {csv_file}")
    print()

    return companies

if __name__ == "__main__":
    search_ems_leads()
