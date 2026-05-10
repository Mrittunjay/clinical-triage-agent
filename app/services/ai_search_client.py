import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from app.config import get_triage_standard

load_dotenv()

class AISearchClient:
    """
    Centralized Azure AI Search Client for Expert RAG.

    Responsibilities:
    - Connect to Azure AI Search
    - Retrieve guidelines based on intake
    - Enforce ATP/NTS protocol filtering
    """

    def __init__(self):
        endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        key = os.getenv("AZURE_SEARCH_KEY")
        index_name = os.getenv("AZURE_SEARCH_INDEX")

        if not endpoint or not key or not index_name:
            raise RuntimeError(
                "Azure AI Search configuration missing."
                "Check AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_KEY, AZURE_SEARCH_INDEX."
            )
        self._client = SearchClient(
            endpoint = endpoint,
            credential = AzureKeyCredential(key),
            index_name = index_name
        )

    def retrieve_guidelines(self, intake: dict, top_k:int = 5) -> list:
        """
        Retrive clinical triage guidelines strictly filtered
        by the active hospital protocol (ATP or NTS)
        """

        # Build a simple, robust query from intake
        chief_complaint = intake.get("chiefComplaint", "")
        symptoms = intake.get("symptoms", [])
        vitals = intake.get("vitals", {})

        query = (
            f"Chief complaint: {chief_complaint}\n"
            f"Symptoms: {symptoms}\n"
            f"Vitals: {vitals}\n"
        )

        # Performing protocol switch
        standard = get_triage_standard().value

        results = list(
            self._client.search(
                # search_text=query,
                search_text=chief_complaint,
                filter=f"standard eq '{standard}'",
                top=top_k
            )
        )

        # UNCOMMENT THE BELOW LINES TO CHECK IF THE SWITCH BETWEEN 
        # ATP AND NTS IS HAPPENING PROPERLY OR NOT.
        # docs = list(results)
        # print("\n********************** Rag Debugging: ************************")
        # print("Standard: ", standard)
        # print("Query:", query)
        # print("Retrieved guidelines IDs: ")
        # for d in docs:
        #     print(" -", d["id"], d["category"], "|", d["triageColor"])

        # Return only guideline text for LLM resoning
        return [doc["content"] for doc in results]