from app.agents.receptionist import normalize_intake
from app.agents.expert_rag import evaluate_triage
from app.agents.librarian_fhir import (fetch_patient_history, 
                                       save_triage_record, 
                                       save_final_decision)
from app.services.content_safety import analyze_text_safety

def run_triage(payload: dict) -> dict:
    """
    Planner agent entry point 
    Coordinates intake, triage reasoning, and EHR update.
    """

    # for now we use fixed patient ID
    patient_id = payload.get("patientId", "patient-001")

    intake = normalize_intake(payload)

    # Apply content safety to patient input
    patient_text = f"{intake.get('chiefComplaint', "")} {' '.join(intake.get('symptoms', []))}"
    input_content_safety = analyze_text_safety(patient_text)

    patient_history = fetch_patient_history(patient_id)

    expert_result = evaluate_triage(intake)

    # Save triage proposal to EHR (pending human approval)
    save_triage_record(patient_id, expert_result)

    return {
        "message":"Planner received triage request",
        "patient_id": patient_id,
        "received_payload": intake,
        "triage_result": expert_result,
        "patient_history": patient_history,
        "input_content_safety": input_content_safety,
        "Human in the loop required": True
    }

def finalize_triage_decision(payload: dict) -> dict:
    """
    Planner handles human approval or override
    """

    patient_id = payload.get("patientId", "patient-001")

    notes = payload.get("notes", "")
    # Apply content safety to human notes
    notes_content_safety = analyze_text_safety(notes) if notes else {"Skipped": True}

    final_decision = {
        "triageColor": payload.get("triageColor"),
        "decisionSource": payload.get("decisionSource"), # "AI_SUGGESTION" or "HUMAN_OVERRIDE"
        "notes": notes  # Clinical truth must remain unaltered so contant safety not used here.
    }

    save_final_decision(patient_id, final_decision)

    print("Human decision received", payload)

    return {
        "message": "Final triage decision recorded",
        "patient_id": patient_id,
        "final_decision": final_decision,
        "notes_content_safety": notes_content_safety    # Safety metadata
    }