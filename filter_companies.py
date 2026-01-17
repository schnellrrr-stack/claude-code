#!/usr/bin/env python
"""Filter companies by employee count range."""
import json
import csv

def filter_companies_by_size(input_json, min_employees=50, max_employees=500):
    """Filter companies to only include those within employee range."""

    # Read JSON file
    with open(input_json, 'r') as f:
        data = json.load(f)

    companies = data.get('companies', [])

    # Filter companies by employee count
    filtered_companies = []
    for company in companies:
        emp_count = company.get('estimated_num_employees', '')

        # Skip if no employee count
        if not emp_count:
            continue

        try:
            emp_count = int(emp_count)
            if min_employees <= emp_count <= max_employees:
                filtered_companies.append(company)
        except (ValueError, TypeError):
            # Skip companies with non-numeric employee counts
            continue

    # Create filtered JSON
    filtered_data = data.copy()
    filtered_data['companies'] = filtered_companies
    filtered_data['total_companies'] = len(filtered_companies)
    filtered_data['filter_applied'] = f"{min_employees}-{max_employees} employees"

    # Save filtered JSON
    output_json = input_json.replace('.json', '_filtered.json')
    with open(output_json, 'w') as f:
        json.dump(filtered_data, f, indent=2)

    print(f"✅ Filtered {len(companies)} companies down to {len(filtered_companies)} companies")
    print(f"   Range: {min_employees}-{max_employees} employees")
    print(f"💾 Saved to: {output_json}")

    # Create CSV
    output_csv = output_json.replace('.json', '.csv')

    fieldnames = [
        'name',
        'website',
        'linkedin_url',
        'twitter_url',
        'facebook_url',
        'phone',
        'industry',
        'estimated_num_employees',
        'city',
        'state',
        'country',
        'postal_code',
        'street_address',
        'founded_year',
        'publicly_traded_symbol',
        'revenue',
        'keywords'
    ]

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for company in filtered_companies:
            # Handle keywords list
            if company.get('keywords'):
                company['keywords'] = '; '.join(company['keywords'])

            # Write row
            row = {k: company.get(k, '') for k in fieldnames}
            writer.writerow(row)

    print(f"💾 CSV saved to: {output_csv}")
    print()

    # Show preview
    print("=" * 60)
    print(f"📋 FILTERED COMPANIES PREVIEW (First 10)")
    print("=" * 60)

    for i, company in enumerate(filtered_companies[:10], 1):
        print(f"\n{i}. {company['name']}")
        if company['industry']:
            print(f"   Industry: {company['industry']}")
        print(f"   Employees: {company['estimated_num_employees']:,}")
        location_parts = [company['city'], company['state'], company['country']]
        location = ', '.join([p for p in location_parts if p])
        if location:
            print(f"   Location: {location}")
        if company['website']:
            print(f"   Website: {company['website']}")

    return output_json, output_csv

if __name__ == "__main__":
    filter_companies_by_size('output/ems_companies_20260117_225004.json')
