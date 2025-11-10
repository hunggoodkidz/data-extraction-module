import re

def extract_number(value):
    """Safely extract a numeric value from a messy string (e.g., '$4.2 billion', '65%')."""
    if not value:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"(\d+(\.\d+)?)", str(value))
    return float(match.group(1)) if match else 0.0