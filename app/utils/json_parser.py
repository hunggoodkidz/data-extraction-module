import re
import json

def parse_ai_json(ai_response: str):
    """
    Extract and clean valid JSON object from AI response.
    Handles markdown fences like ```json ... ``` and returns a dict.
    """
    # Remove Markdown-style fences like ```json ... ```
    cleaned = re.sub(r"^```json|```$", "", ai_response.strip(), flags=re.MULTILINE).strip()
    cleaned = re.sub(r"^```|```$", "", cleaned.strip(), flags=re.MULTILINE).strip()

    # Extract the JSON object part
    json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not json_match:
        raise ValueError("No JSON object found in AI response.")

    json_str = json_match.group().strip()
    try:
        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Failed to parse cleaned JSON: {e}\nRaw: {json_str[:300]}")