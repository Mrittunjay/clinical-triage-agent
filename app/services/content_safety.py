import os
import requests
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

CONTENT_SAFETY_ENDPOINT= os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
CONTENT_SAFETY_KEY= os.getenv("AZURE_CONTENT_SAFETY_KEY")

# Date based api versioning (Azure AI Content Safety REST API specification)
API_VERSION = "2023-10-01"

def analyze_text_safety(text: str) -> dict:
    """
    Analyze text using Azure AI Content Safety
    Sends text to Azure AI Content Safety and 
    returns a structured risk assessment of that text. It does not modify the text.
    """
    if not text:
        return {"Skipped": True, "reason": "empty input"}
    
    url = f"{CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version={API_VERSION}"

    headers = {
        # "Ocp-Apim-Subscription-key" - "API Management" - "Subscription-key"
        # standard HTTP authentication header used by Azure Cognitive Services (including Azure AI Content Safety).
        "Ocp-Apim-Subscription-key": CONTENT_SAFETY_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "categories": ["Hate", "Sexual", "Violence", "SelfHarm"]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()     # Raises :class:`HTTPError`, if one occurred.

    return response.json()