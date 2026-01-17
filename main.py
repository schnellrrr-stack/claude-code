# main.py
import json
import sys
import os
from datetime import datetime
from apollo_connector import ApolloConnector
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY

class LeadGenerator:
    def __init__(self):
        self.apollo = ApolloConnector()
        # Handle automatic API key detection
        api_key = ANTHROPIC_API_KEY
        if api_key == "this_is_handled_automatically":
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.claude = Anthropic(api_key=api_key)

    def parse_icp_with_claude(self, icp_description):
        """
        Use Claude to parse natural language ICP into structured criteria
        """
        print("🤖 Parsing ICP with Claude...")

        prompt = f"""Parse this ICP (Ideal Customer Profile) description into structured search criteria for Apollo.io API.

ICP Description: {icp_description}

Return ONLY valid JSON with these fields (use empty arrays if not specified):
{{
    "job_titles": ["exact job titles like 'CTO', 'VP Engineering'"],
    "seniority_levels": ["C-Suite", "VP", "Director", "Manager"],
    "company_size": ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5001+"],
    "industries": ["industry keywords"],
    "locations": ["city, state or country names"]
}}

Be specific with job titles and use standard Apollo.io format."""

        message = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract JSON from Claude's response
        response_text = message.content[0].text

        # Find JSON in response (handle markdown code blocks)
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()

        try:
            criteria = json.loads(json_str)
            print(f"✅ Parsed criteria: {json.dumps(criteria, indent=2)}")
            return criteria
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing Claude's response: {e}")
            print(f"Response was: {response_text}")
            return None

    def generate_leads(self, icp_description):
        """
        Main function to generate leads from ICP description
        """
        print("\n" + "="*60)
        print("🚀 LEAD GENERATION STARTED")
        print("="*60 + "\n")

        # Step 1: Parse ICP
        criteria = self.parse_icp_with_claude(icp_description)
        if not criteria:
            print("❌ Failed to parse ICP. Exiting.")
            return

        # Step 2: Search Apollo
        print("\n📊 Searching Apollo.io for leads...")
        raw_results = self.apollo.search_people(criteria)

        if not raw_results:
            print("❌ No results from Apollo. Check your API key and criteria.")
            return

        # Step 3: Format results
        leads = self.apollo.format_leads(raw_results)
        print(f"✅ Found {len(leads)} leads")

        # Step 4: Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/leads_{timestamp}.json"

        output_data = {
            "generated_at": datetime.now().isoformat(),
            "icp_description": icp_description,
            "criteria_used": criteria,
            "total_leads": len(leads),
            "leads": leads
        }

        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=2)

        print(f"\n💾 Results saved to: {output_file}")

        # Display preview
        print("\n" + "="*60)
        print("📋 LEAD PREVIEW (First 3)")
        print("="*60)
        for i, lead in enumerate(leads[:3], 1):
            print(f"\n{i}. {lead['first_name']} {lead['last_name']}")
            print(f"   Title: {lead['title']}")
            print(f"   Company: {lead['company_name']}")
            print(f"   Email: {lead['email']}")
            print(f"   LinkedIn: {lead['linkedin_url']}")

        print("\n" + "="*60)
        print("✅ LEAD GENERATION COMPLETED")
        print("="*60 + "\n")

        return leads

def main():
    # Check if ICP description provided
    if len(sys.argv) < 2:
        print("Usage: python main.py '<ICP description>'")
        print("\nExample:")
        print('python main.py "CTOs and VPs of Engineering at B2B SaaS companies with 50-500 employees in the United States"')
        sys.exit(1)

    icp_description = " ".join(sys.argv[1:])

    generator = LeadGenerator()
    generator.generate_leads(icp_description)

if __name__ == "__main__":
    main()
