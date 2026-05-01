# Simulated in-memory EHR store (temporary)
_FAKE_EHR_DB = {
    "patient-001": {
        "conditions": ["hypertention"],
        "last_visit": "2025-11-10"
    }
}

def fetch_patient_history(patient_id: str) -> dict:
    """
    Librarian agent:
    Fetch patient history from EHR (FHIR).
    Currently simulated.
    """
    return _FAKE_EHR_DB.get(patient_id, {})

def save_triage_record(patient_id: str, triage_result: dict) -> None:
    """
    Librarian agent:
    Save triage decision to EHR.
    Currently simulated.
    """
    _FAKE_EHR_DB[patient_id] = {
        **_FAKE_EHR_DB.get(patient_id, {}),
        "last_triage": triage_result
    }

def save_final_decision(patient_id: str, final_decision: dict) -> None:
    """
    Save the final (human-approved or overridden) triage decision.
    """
    _FAKE_EHR_DB[patient_id] = {
        **_FAKE_EHR_DB.get(patient_id, {}),
        "final_triage": final_decision
    }