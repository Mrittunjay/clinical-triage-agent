# Data ingestion mechanism for RAG expert agent
# Using official Azure AI Search SDK classes
import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
load_dotenv()

# Read environmental variables
SEARCH_ENDPOINT= os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX")

# Creating a search client
# This client directly talks to our index
# Same oject will later be used by the Expert Agent to retrieve docs
client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(SEARCH_KEY),
)

# Export guideline documents (authoritative, short, explicit)
# These are export facts, each document here encodes one decision rule,
# For now this is small and testable
documents = [
    {
        "id": "triage_cp_001",
        "content": "Chest pain with shortness of breath should be triaged RED because of high cardiac risk.",
        "triageColor": "RED",
        "category": "Chest Pain",
        "source": "Emergency Triage Guideline v3.2",
    },
    {
        "id": "vitals_spo2_001",
        "content": "SpO2 below 93 percent in adults indicates high risk and requires urgent evaluation.",
        "triageColor": "RED",
        "category": "Vitals",
        "source": "Respiratory Triage Standards",
    },
    {
        "id": "general_lowrisk_001",
        "content": "Patients with mild symptoms and stable vital signs may be triaged GREEN.",
        "triageColor": "GREEN",
        "category": "General",
        "source": "General Triage Guidelines",
    },
]

# Upload documents to Azure AI search -> Calls Azure Search indexing API
# Azure then handles batching, validation and storage
result = client.upload_documents(documents)

# Print upload status 
for r in result:
    print(f"Document {r.key} uploaded: {r.succeeded}")

# Run this script in terminal for data ingestion.
