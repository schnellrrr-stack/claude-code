#!/usr/bin/env python
"""Generate leads for EMS manufacturing companies."""
import json
from datetime import datetime
from apollo_connector import ApolloConnector

def generate_ems_leads():
    """Generate leads for EMS manufacturing companies in the United States."""
    print("=" * 60)
    print("🔍 EMS MANUFACTURING LEAD GENERATION")
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
            "EMS",
            "Electronics Manufacturing",
            "Electronics Manufacturing Services",
            "Contract Manufacturing",
            "Electronic Contract Manufacturing",
            "Electronics",
            "Electrical/Electronic Manufacturing",
            "PCB Manufacturing",
            "Printed Circuit Boards",
            "Assembly Manufacturing"
        ],
        "locations": [
            "United States"
        ]
    }

    print("📋 Search Criteria:")
    print(f"   Industry: EMS Manufacturing Companies")
    print(f"   Company Size: 50-500 employees")
    print(f"   Location: United States")
    print()
    print("   Detailed criteria:")
    print(json.dumps(criteria, indent=2))
    print()

    # Search Apollo for companies
    print("📊 Searching Apollo.io for EMS manufacturing companies...")
    raw_results = apollo.search_organizations(criteria=criteria, per_page=100)

    if raw_results.get("error"):
        print(f"❌ Error: {raw_results.get('message')}")
        if raw_results.get('status_code'):
            print(f"   Status Code: {raw_results.get('status_code')}")
        return

    # Format results
    companies = apollo.format_companies(raw_results)
    print(f"✅ Found {len(companies)} companies on this page")

    # Get pagination info
    pagination = raw_results.get("pagination", {})
    total_available = pagination.get('total_entries', 0)
    print(f"   Total available in Apollo: {total_available:,}")
    print()

    # Save results to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_output_file = f"output/ems_leads_{timestamp}.json"

    output_data = {
        "generated_at": datetime.now().isoformat(),
        "description": "EMS Manufacturing Companies - United States - 50-500 employees",
        "criteria_used": criteria,
        "total_companies_found": len(companies),
        "total_available_in_apollo": total_available,
        "companies": companies
    }

    with open(json_output_file, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"💾 JSON results saved to: {json_output_file}")

    # Also save as CSV for easy import to CRM
    csv_output_file = f"output/ems_leads_{timestamp}.csv"
    save_to_csv(companies, csv_output_file)
    print(f"💾 CSV results saved to: {csv_output_file}")
    print()

    # Display preview
    print("=" * 60)
    print(f"📋 COMPANY PREVIEW (First {min(10, len(companies))} of {len(companies)})")
    print("=" * 60)

    for i, company in enumerate(companies[:10], 1):
        print(f"\n{i}. {company['name']}")
        if company['industry']:
            print(f"   Industry: {company['industry']}")
        if company['estimated_num_employees']:
            print(f"   Size: {company['estimated_num_employees']:,} employees")
        else:
            print(f"   Size: Unknown")
        location_parts = [p for p in [company['city'], company['state'], company['country']] if p]
        if location_parts:
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
    print("✅ LEAD GENERATION COMPLETED")
    print("=" * 60)
    print()
    print(f"📊 Summary:")
    print(f"   - {len(companies)} companies retrieved")
    print(f"   - {total_available:,} total companies available in Apollo")
    print(f"   - Results saved to: {json_output_file}")
    print(f"   - CSV exported to: {csv_output_file}")

    return companies


def save_to_csv(companies, filename):
    """Save companies to CSV file."""
    import csv

    if not companies:
        return

    # Define CSV columns
    fieldnames = [
        'name',
        'website',
        'phone',
        'industry',
        'industries',
        'keywords',
        'estimated_num_employees',
        'city',
        'state',
        'country',
        'postal_code',
        'street_address',
        'founded_year',
        'revenue',
        'linkedin_url',
        'twitter_url',
        'facebook_url',
        'publicly_traded_symbol'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for company in companies:
            # Convert list fields to comma-separated strings
            row = company.copy()
            if isinstance(row.get('industries'), list):
                row['industries'] = ', '.join(row['industries'])
            if isinstance(row.get('keywords'), list):
                row['keywords'] = ', '.join(row['keywords'])

            writer.writerow(row)


if __name__ == "__main__":
    generate_ems_leads()
