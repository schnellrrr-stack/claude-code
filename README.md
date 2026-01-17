# AI-Powered Lead Generation System

An intelligent lead generation system that combines Apollo.io's B2B database with Claude AI to parse natural language Ideal Customer Profiles (ICPs) and generate targeted lead lists.

## Features

- **Natural Language ICP Parsing**: Describe your ideal customer in plain English, and Claude AI converts it into structured search criteria
- **Apollo.io Integration**: Leverage Apollo's extensive B2B database for accurate lead data
- **Automated Lead Enrichment**: Get complete contact information including emails, LinkedIn profiles, and phone numbers
- **Structured Output**: Results saved as JSON with timestamps for easy tracking

## Tech Stack

- **Python 3.8+**
- **Apollo.io API**: B2B lead database
- **Anthropic Claude API**: Natural language processing
- **Pydantic**: Configuration management and validation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd claude-code
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` and add your API keys:
```
APOLLO_API_KEY=your_apollo_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Usage

Run the lead generator with a natural language ICP description:

```bash
python main.py "CTOs and VPs of Engineering at B2B SaaS companies with 50-500 employees in the United States"
```

### Example ICPs

```bash
# Target tech executives
python main.py "Chief Technology Officers at fintech companies with 100-1000 employees"

# Target marketing leaders
python main.py "VP of Marketing and CMOs at e-commerce companies in California"

# Target specific industries
python main.py "Directors of Sales at healthcare software companies with 200+ employees"
```

## How It Works

1. **ICP Parsing**: Claude AI analyzes your natural language description and extracts:
   - Job titles
   - Seniority levels
   - Company size ranges
   - Industries
   - Locations

2. **Lead Search**: The system queries Apollo.io's API with the structured criteria

3. **Result Formatting**: Raw API responses are cleaned and formatted into a standardized structure

4. **Output**: Results are saved to `output/leads_TIMESTAMP.json` with metadata

## Output Format

```json
{
  "generated_at": "2025-01-17T10:30:00",
  "icp_description": "CTOs at B2B SaaS companies...",
  "criteria_used": {
    "job_titles": ["CTO", "Chief Technology Officer"],
    "company_size": ["50-200", "201-500"],
    "industries": ["Computer Software", "SaaS"]
  },
  "total_leads": 25,
  "leads": [
    {
      "first_name": "John",
      "last_name": "Doe",
      "title": "Chief Technology Officer",
      "email": "john.doe@company.com",
      "linkedin_url": "https://linkedin.com/in/johndoe",
      "company_name": "Example SaaS Inc",
      "company_website": "https://example.com",
      "company_industry": "Computer Software",
      "company_size": "150"
    }
  ]
}
```

## File Structure

```
.
├── main.py                 # Main entry point
├── apollo_connector.py     # Apollo.io API integration
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── .env                  # Your API keys (create from .env.example)
├── output/               # Generated lead files
└── README.md            # This file
```

## API Keys

### Apollo.io API Key
1. Sign up at [Apollo.io](https://www.apollo.io/)
2. Navigate to Settings > API
3. Generate a new API key

### Anthropic API Key
1. Sign up at [Anthropic](https://www.anthropic.com/)
2. Navigate to API Keys
3. Generate a new API key

## Configuration

Advanced configuration options in `.env`:

```bash
# Default search parameters (optional)
DEFAULT_PERSON_TITLES=CEO,CTO,VP Engineering
DEFAULT_COMPANY_SIZE=1-10,11-50,51-200
DEFAULT_INDUSTRY=Computer Software,Information Technology

# Output settings
OUTPUT_FORMAT=json
MAX_RESULTS=100
```

## Limitations

- Apollo.io API rate limits apply
- Some contact information may be unavailable depending on your Apollo subscription tier
- Claude AI parsing accuracy depends on ICP description clarity

## License

MIT License
