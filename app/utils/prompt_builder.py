def build_fund_company_prompt(preview_text: str) -> str:
    """AI prompt to extract fund and company names."""
    return f"""
You are an AI that extracts key identifying information from investment reports.

Extract ONLY the fund and company names in valid JSON format:
{{
  "fund_name": "",
  "company_name": ""
}}

Text:
{preview_text}
"""

def build_company_prompt(raw_text: str) -> str:
    return f"""
You are a strict data extraction AI.
Return ONLY a single valid JSON object. No explanations, no markdown, no text outside JSON.

Extract these fields from the report:
{{
  "company_name": "",
  "holding_company": "",
  "business_description": "",
  "head_office_location": "",
  "fund_role": "",
  "investment_type": "",
  "ownership_percent": "",
  "first_completion_date": "",
  "transaction_value": "",
  "current_cost": "",
  "fair_value": ""
}}

Do not include words like 'Here is' or 'Sure'.
Only output valid JSON.

Text:
{raw_text}
"""

def build_financial_prompt(raw_text: str) -> str:
    return f"""
You are an AI that extracts company financial highlights from an annual report.

Extract ONLY these fields in valid JSON format:
{{
  "period": "",
  "currency": "",
  "revenue": "",
  "ebitda": "",
  "ebitda_margin": "",
  "ebit": "",
  "ebit_margin": "",
  "net_profit_after_tax": "",
  "capex": "",
  "net_debt": ""
}}

Use only exact numbers from the text below. Do not guess.
Output valid JSON only.

Text:
\"\"\"{raw_text}\"\"\"
"""