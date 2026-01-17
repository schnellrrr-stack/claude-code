#!/usr/bin/env python
"""Test Apollo.io integration directly without Claude AI parsing."""
import json
from datetime import datetime
from apollo_connector import ApolloConnector

def test_apollo_search():
    """Test Apollo company search with manual criteria."""
    print("=" * 60)
    print("🧪 APOLLO.IO TEST - Company Search")
    print("=" * 60)
    print()

    # Initialize Apollo connector
    apollo = ApolloConnector()

    # Define search criteria for companies
    criteria = {
        "company_size": [
            "11-50",
            "51-200",
            "201-500"
        ],
        "industries": [
            "SaaS",
            "eCommerce",
            "E-commerce",
            "Software",
            "Internet"
        ],
        "locations": [
            "Germany"
        ]
    }

    print("📋 Search Criteria:")
    print(json.dumps(criteria, indent=2))
    print()

    # Search Apollo for companies
    print("📊 Searching Apollo.io for companies...")
    raw_results = apollo.search_organizations(criteria=criteria, per_page=25)

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
    print(f"   Total available: {pagination.get('total_entries', 'Unknown'):,}")
    print()

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output/test_companies_{timestamp}.json"

    output_data = {
        "generated_at": datetime.now().isoformat(),
        "test_description": "Direct Apollo.io test - SaaS/eCommerce companies in Germany",
        "criteria_used": criteria,
        "total_companies": len(companies),
        "total_available": pagination.get('total_entries', 0),
        "companies": companies
    }

    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"💾 Results saved to: {output_file}")
    print()

    # Display preview
    print("=" * 60)
    print("📋 COMPANY PREVIEW (First 5)")
    print("=" * 60)

    for i, company in enumerate(companies[:5], 1):
        print(f"\n{i}. {company['name']}")
        print(f"   Industry: {company['industry']}")
        print(f"   Size: {company['estimated_num_employees']:,} employees" if company['estimated_num_employees'] else f"   Size: Unknown")
        print(f"   Location: {company['city']}, {company['country']}")
        print(f"   Website: {company['website']}")
        print(f"   Founded: {company['founded_year']}")
        print(f"   Revenue: {company['revenue']}")
        if company.get('keywords'):
            print(f"   Keywords: {', '.join(company['keywords'][:5])}")

    print()
    print("=" * 60)
    print("✅ TEST COMPLETED")
    print("=" * 60)

    return companies

if __name__ == "__main__":
    test_apollo_search()
