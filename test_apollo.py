#!/usr/bin/env python
"""Test Apollo.io integration directly without Claude AI parsing."""
import json
from datetime import datetime
from apollo_connector import ApolloConnector

def test_apollo_search():
    """Test Apollo search with manual criteria."""
    print("=" * 60)
    print("🧪 APOLLO.IO TEST - Direct Search")
    print("=" * 60)
    print()

    # Initialize Apollo connector
    apollo = ApolloConnector()

    # Define search criteria manually
    criteria = {
        "job_titles": [
            "Head of Marketing",
            "Director of Marketing",
            "VP Marketing",
            "Head of SEO",
            "Director of SEO",
            "SEO Manager",
            "Growth Marketing Manager",
            "Demand Gen Manager",
            "Content Lead",
            "Digital Marketing Manager"
        ],
        "company_size": [
            "11-50",
            "51-200",
            "201-500"
        ],
        "industries": [
            "SaaS",
            "eCommerce",
            "E-commerce",
            "Software"
        ],
        "locations": [
            "Germany"
        ]
    }

    print("📋 Search Criteria:")
    print(json.dumps(criteria, indent=2))
    print()

    # Search Apollo
    print("📊 Searching Apollo.io...")
    raw_results = apollo.search_people(criteria=criteria, per_page=25)

    if raw_results.get("error"):
        print(f"❌ Error: {raw_results.get('message')}")
        if raw_results.get('status_code'):
            print(f"   Status Code: {raw_results.get('status_code')}")
        return

    # Format results
    leads = apollo.format_leads(raw_results)
    print(f"✅ Found {len(leads)} leads")
    print()

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output/test_leads_{timestamp}.json"

    output_data = {
        "generated_at": datetime.now().isoformat(),
        "test_description": "Direct Apollo.io test - Marketing roles in Germany",
        "criteria_used": criteria,
        "total_leads": len(leads),
        "leads": leads
    }

    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"💾 Results saved to: {output_file}")
    print()

    # Display preview
    print("=" * 60)
    print("📋 LEAD PREVIEW (First 5)")
    print("=" * 60)

    for i, lead in enumerate(leads[:5], 1):
        print(f"\n{i}. {lead['first_name']} {lead['last_name']}")
        print(f"   Title: {lead['title']}")
        print(f"   Company: {lead['company_name']}")
        print(f"   Industry: {lead['company_industry']}")
        print(f"   Size: {lead['company_size']} employees")
        print(f"   Location: {lead['company_location']}")
        print(f"   Email: {lead['email']}")
        print(f"   LinkedIn: {lead['linkedin_url']}")

    print()
    print("=" * 60)
    print("✅ TEST COMPLETED")
    print("=" * 60)

    return leads

if __name__ == "__main__":
    test_apollo_search()
