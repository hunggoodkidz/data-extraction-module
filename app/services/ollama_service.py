import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def call_ollama(prompt: str, model: str = "phi3"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json().get("response", "")
