#!/usr/bin/env python
"""
Generic company search script - customize for your ICP.

Example usage:
    python search_companies.py

Edit the parameters below to match your ICP criteria.
"""
from search_ems_companies import search_companies

# ============================================================
# CUSTOMIZE YOUR ICP CRITERIA HERE
# ============================================================

# Example 1: EMS Manufacturing Companies
industries = [
    "Electronics Manufacturing",
    "EMS",
    "Contract Manufacturing",
    "PCB Assembly"
]
min_employees = 50
max_employees = 500
locations = ["United States"]
description = "EMS Manufacturing Companies"

# Example 2: SaaS Companies (uncomment to use)
# industries = ["SaaS", "Software", "Cloud Computing"]
# min_employees = 100
# max_employees = 1000
# locations = ["United States", "Canada"]
# description = "B2B SaaS Companies"

# Example 3: Healthcare Technology (uncomment to use)
# industries = ["Healthcare", "Health Tech", "Medical Devices"]
# min_employees = 200
# max_employees = 2000
# locations = ["California", "Massachusetts", "Texas"]
# description = "Healthcare Technology Companies"

# ============================================================
# RUN THE SEARCH
# ============================================================

if __name__ == "__main__":
    search_companies(
        industries=industries,
        min_employees=min_employees,
        max_employees=max_employees,
        locations=locations,
        description=description
    )
