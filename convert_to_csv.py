#!/usr/bin/env python
"""Convert company JSON results to CSV format."""
import json
import csv
from pathlib import Path

def json_to_csv(json_file, csv_file=None):
    """Convert company JSON to CSV."""
    # Read JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    companies = data.get('companies', [])

    if not companies:
        print("No companies found in JSON file")
        return

    # Generate CSV filename if not provided
    if csv_file is None:
        csv_file = json_file.replace('.json', '.csv')

    # Define CSV columns
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

    # Write CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for company in companies:
            # Handle keywords list - join with semicolons
            if company.get('keywords'):
                company['keywords'] = '; '.join(company['keywords'])

            # Handle industries list
            if isinstance(company.get('industries'), list):
                company['industries_list'] = '; '.join(company['industries'])

            # Write row (only fields in fieldnames)
            row = {k: company.get(k, '') for k in fieldnames}
            writer.writerow(row)

    print(f"✅ Converted {len(companies)} companies to CSV")
    print(f"💾 Saved to: {csv_file}")
    return csv_file

if __name__ == "__main__":
    # Find the most recent JSON file in output directory
    output_dir = Path("output")
    json_files = list(output_dir.glob("test_companies_*.json"))

    if not json_files:
        print("❌ No company JSON files found in output directory")
    else:
        # Get most recent file
        latest_json = max(json_files, key=lambda p: p.stat().st_mtime)
        print(f"📄 Converting: {latest_json}")
        print()
        json_to_csv(str(latest_json))
