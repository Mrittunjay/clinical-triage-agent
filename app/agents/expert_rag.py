"""
Expert Agent: Clinical Triage Authority

Responsibilities:
- Perform deterministic, rule-based triage (existing logic)
- Augment decisions with guideline-based RAG (Azure AI Search)
- Return a single expert recommendation to the Planner
"""
from app.services.ai_search_client import AISearchClient
from app.services.openai_client import planner_llm

_search_client = AISearchClient()


# Rule based fallback expert (safety-first, deterministic)
def evaluate_triage(intake: dict) -> dict:
    """
    Deterministic fallback triage logic.
    Used ONLY when guideline-based RAG is unavailable or fails.

    This logic is:
    - conservative
    - physiology-first
    - explicitly labeled as fallback
    """

    print("**************** FALLBACK TRIAGE ACTIVE ****************")

    vitals = intake.get("vitals", {}) or {}
    symptoms = intake.get("symptoms", []) or []
    chief_complaint = intake.get("chiefComplaint", "").lower()

    heart_rate = vitals.get("heartRate")
    spo2 = vitals.get("spo2")

    # life-threatening = RED
    # Hypoxia
    if spo2 is not None and spo2 < 90:
        return {
            "triageColor": "RED",
            "reason": "Low oxygen saturation detected in fallback triage",
            "suggestedTests": [],
            "source": "RuleBasedFallback"
        }

    # Airway risk keywords
    airway_keywords = [
        "swollen throat",
        "neck swelling",
        "difficulty breathing",
        "difficulty swallowing",
        "stridor"
    ]
    if any(k in chief_complaint for k in airway_keywords) or \
       any(k in " ".join(symptoms).lower() for k in airway_keywords):
        return {
            "triageColor": "RED",
            "reason": "Possible airway compromise detected in fallback triage",
            "suggestedTests": [],
            "source": "RuleBasedFallback"
        }

    # Severe tachycardia
    if heart_rate is not None and heart_rate > 130:
        return {
            "triageColor": "RED",
            "reason": "Severely elevated heart rate detected in fallback triage",
            "suggestedTests": [],
            "source": "RuleBasedFallback"
        }

    # symptomatic but stable = YELLOW
    if symptoms:
        return {
            "triageColor": "YELLOW",
            "reason": "Symptoms present without critical instability (fallback triage)",
            "suggestedTests": [],
            "source": "RuleBasedFallback"
        }

    # No concerning features = GREEN
    return {
        "triageColor": "GREEN",
        "reason": "No significant symptoms or vital sign abnormalities detected (fallback triage)",
        "suggestedTests": [],
        "source": "RuleBasedFallback"
    }

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

    guidelines = _search_client.retrieve_guidelines(intake)

    if guidelines:
        try:
            return _rag_expert_decision(guidelines)
        except Exception:
            # Fail safe: never block triage if RAG fails
            print("Exception in rag_expert_decision")

    # Conservative fallback
    return evaluate_triage(intake)

