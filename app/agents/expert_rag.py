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
