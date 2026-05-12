from fastapi import FastAPI
from app.planner import run_triage, finalize_triage_decision
from typing import Dict, List
from uuid import uuid4
from app.agents.receptionist import conversational_intake
from app.planner import run_triage
# FastAPI uses Starlette’s StaticFiles to serve HTML, JS, CSS, etc.
# To serve static files inside 'ui' folder.
from fastapi.staticfiles import StaticFiles
from app.config import get_triage_standard, set_triage_standard

# Simple in-memory intake session
INTAKE_SESSIONS: Dict[str, List[Dict[str, str]]] = {}

app = FastAPI(title="Multi Agent Patient Triage and Care Coordination")

# Serve UI files
app.mount("/ui", StaticFiles(directory="ui", html=True), name="ui")

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/triage")
def triage(payload: dict):
    return run_triage(payload)

@app.post("/triage/decision")
def triage_decision(payload: dict):
    return finalize_triage_decision(payload)

@app.post("/intake/start")
def start_intake():
    """
    Starts a new patient intake conversation
    UI will call this when start intake buttion is clicked
    """
    # Use random number generator to create an ID
    session_id = str(uuid4())

    # Initialize empty chat history
    INTAKE_SESSIONS[session_id] = []

    first_question = "What problem are you facing ?"

    # Store assistant message
    INTAKE_SESSIONS[session_id].append({
        "role": "assistant",
        "content": first_question
    })

    return {
        "sessionId": session_id,
        "message": first_question
    }

@app.post("/intake/message")
def intake_message(payload: Dict[str, str]):
    """
    Handles next patient message in intake conversation.
    """
    session_id = payload.get("sessionId")
    patient_message = payload.get("message")

    if session_id not in INTAKE_SESSIONS:
        return {"error": "Invalid or expired session"}
    
    # Append patient message
    INTAKE_SESSIONS[session_id].append({
        "role": "patient",
        "content": patient_message
    })

    # call receptionist agent
    receptionist_response = conversational_intake(INTAKE_SESSIONS[session_id])

    if receptionist_response["status"] == "IN_PROGRESS":
        # store assistant message
        INTAKE_SESSIONS[session_id].append({
            "role": "assistant",
            "content": receptionist_response["message"]
        })

        return {
            "status": "IN_PROGRESS",
            "message": receptionist_response["message"]
        }
    
    # Intake complete -> now handoff to planner
    intake = receptionist_response["intake"]

    # Attach patient ID
    intake["patientId"] = session_id

    triage_result = run_triage(intake)

    # Cleanup 
    INTAKE_SESSIONS.pop(session_id, None)

    return {
        "status": "COMPLETE",
        **triage_result
        # "intake": intake,
        # "triageResult": triage_result
    }

@app.get("/admin/config")
def read_config():
    return {"triageStandard": get_triage_standard().value}

@app.post("/admin/config")
def update_config(payload: dict):
    set_triage_standard(payload["triageStandard"])
    return {"status": "updated"}
