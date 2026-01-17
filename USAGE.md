# Lead Generation Usage Guide

## Quick Start

### Option 1: Default EMS Search (50-500 employees)
```bash
python search_ems_companies.py
```

### Option 2: Custom ICP Search
Edit `search_companies.py` and customize your criteria:

```python
industries = ["Your", "Industry", "Keywords"]
min_employees = 100
max_employees = 1000
locations = ["United States", "Canada"]
description = "Your ICP Description"
```

Then run:
```bash
python search_companies.py
```

## ICP Parameters

### Industries
List of industry keywords to search for:
```python
industries = [
    "Electronics Manufacturing",
    "EMS",
    "Contract Manufacturing"
]
```

### Employee Count
Specify exact min and max employee range:
```python
min_employees = 50   # Minimum company size
max_employees = 500  # Maximum company size
```

### Locations
List of geographic locations (countries, states, or cities):
```python
locations = ["United States"]
# or
locations = ["California", "Texas", "New York"]
# or
locations = ["United States", "Canada", "United Kingdom"]
```

## Example ICPs

### 1. EMS Manufacturing (Default)
```python
industries = ["Electronics Manufacturing", "EMS", "Contract Manufacturing"]
min_employees = 50
max_employees = 500
locations = ["United States"]
```

### 2. Mid-Market SaaS
```python
industries = ["SaaS", "Software", "Cloud Computing", "B2B Software"]
min_employees = 100
max_employees = 1000
locations = ["United States", "Canada"]
```

### 3. Healthcare Technology
```python
industries = ["Healthcare", "Health Tech", "Medical Devices", "Telehealth"]
min_employees = 200
max_employees = 2000
locations = ["California", "Massachusetts", "New York"]
```

### 4. FinTech Startups
```python
industries = ["FinTech", "Financial Services", "Payment Processing", "Blockchain"]
min_employees = 20
max_employees = 200
locations = ["New York", "San Francisco", "London"]
```

## Output Options

After the search completes, you'll be asked:
```
📥 Do you want to export results to CSV? (yes/no):
```

- Type **`yes`** or **`y`**: Displays CSV data in console (copy/paste it)
- Type **`no`** or **`n`**: Shows summary only, no CSV export

## Tips

1. **Industry Keywords**: Use Apollo.io's industry taxonomy. Common keywords work well (e.g., "Manufacturing", "SaaS", "Healthcare")

2. **Employee Ranges**: The script maps your exact range to Apollo's buckets:
   - 1-10, 11-50, 51-200, 201-500, 501-1000, 1001-5000, 5001+

3. **Locations**: Can be specific (city/state) or broad (country)

4. **Results Limit**: Currently returns up to 100 companies per search

## Files Generated

The script doesn't automatically save files. When you choose to export CSV:
- CSV content is displayed in the console
- Copy and paste the output into a text editor
- Save as `.csv` file
