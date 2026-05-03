"""
Expert Agent: Clinical Triage Authority

Responsibilities:
- Perform deterministic, rule-based triage (existing logic)
- Augment decisions with guideline-based RAG (Azure AI Search)
- Return a single expert recommendation to the Planner
"""

import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from app.services.openai_client import planner_llm

# Azure AI search configuration(Expert Knowledge Store)
_SEARCH_ENDPOINT= os.getenv("AZURE_SEARCH_ENDPOINT")
_SEARCH_KEY=os.getenv("AZURE_SEARCH_KEY")
_INDEX_NAME=os.getenv("AZURE_SEARCH_INDEX")

_search_client = SearchClient(
    endpoint=_SEARCH_ENDPOINT,
    index_name=_INDEX_NAME,
    credential=AzureKeyCredential(_SEARCH_KEY)
)

# Existing rule-based expert, temporary
def evaluate_triage(intake: dict) -> dict:
    """
    Expert agent:
    - Performs clinical triage resoning 
    - Uses deterministic rules (no AI yet)
    """

    vitals = intake.get("vitals", {})
    symptoms = intake.get("symptoms", [])

    heart_rate = vitals.get("heartRate", -1)
    spo2 = vitals.get("spo2", -1)

    # RED Criteria
    if spo2 < 94 or heart_rate > 100 or "chest pain" in intake.get("chiefComplaint", ""):
        return {
            "triageColor": "RED",
            "reason": "High-risk vitals or symptoms detected",
            "suggestedTests": ["ECG", "Troponin"]
        }

    # YELLOW Criteria
    if symptoms:
        return {
            "triageColor": "YELLOW",
            "reason": "Symptoms present but vitals stable", 
            "suggestedTests": ["ECG"]
        }

    # GREEN Criteria
    return {
        "triageColor": "GREEN",
        "reason": "Vitals and presentation within normal limits",
        "suggestedTests": []
    }

# RAG: Guideline Retrieval (No LLM)

def _retrieve_guidelines(intake: dict, top_k: int = 5) -> list[str]:
    """
    Retrieve relevant triage guidelines from Azure AI Search
    """

    query = f"{intake.get('chiefComplaint', '')} {' '.join(intake.get('symptoms', []))}"

    results = _search_client.search(
        search_text=query,
        top=top_k,
    )

    return [doc["content"] for doc in results]


# RAG: LLM-Based expert decision (strictly grounded)
def _rag_expert_decision(guidelines: list[str]) -> dict:
    """
    Uses LLM only to interpret retrived guidelines.
    The LLM is not allowed to infer beyond provided text.
    """


    prompt = f"""
        You are a clinical triage expert.

        Only use the guidelines below.
        Do NOT infer, assume, or add medical knowledge.

        Guidelines:
        {chr(10).join(guidelines)}

        Return JSON only in this format:
        {{
        "triageColor": "RED | YELLOW | GREEN",
        "reason": "...",
        "suggestedTests": [...],
        "source": "guideline name or description"
        }}
    """
    response = planner_llm(prompt)
    return response


# Public API: Unified expert agent entry point
def expert_triage(intake: dict) -> dict:
    """
    Unified expert agent used by the planner

    Order of execution:
    1. Attempt guideline-based (RAG) evaluation
    2. If no guidelines retrieved, fall back to rule-based expert
    """

    guidelines = _retrieve_guidelines(intake)

    if guidelines:
        try:
            return _rag_expert_decision(guidelines)
        except Exception:
            # Fail safe: never block triage if RAG fails
            pass

    # Conservative fallback
    return evaluate_triage(intake)

