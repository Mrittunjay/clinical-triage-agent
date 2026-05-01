from fastapi import FastAPI
from app.planner import run_triage, finalize_triage_decision

app = FastAPI(title="Multi Agent Patient Triage and Care Coordination")

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/triage")
def triage(payload: dict):
    return run_triage(payload)

@app.post("/triage/decision")
def triage_decision(payload: dict):
    return finalize_triage_decision(payload)
