# Addes conversational intake with Azure OpenAI
# Produces output in the same structure as the Planner agent expects

from typing import List, Dict, Any
from app.services.openai_client import planner_llm
import json

def normalize_intake(payload: dict) -> dict:
    """
    Receprionist agent:
    - Cleans and normalizes patient intake data
    - Ensures palnner receives structured input
    """

    return {
        # get() safely pulls information from a dictionary. checks for each level and 
        # returns empty string or list(the 2nd argument), and the program does not cresh.
        "chiefComplaint": payload.get("chiefComplaint", "").strip().lower(),
        "symptoms": payload.get("symptoms", []),
        "vitals": payload.get("vitals", {}),
        "demographics": payload.get("demographics", {})
    }


def conversational_intake(chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
    
    """
    Conversational receptionist agent.

    Input:
    chat_history: list of {role: "patient" | "assistant", content: str}

    Output:
    Either:
        A) A question string (intake still in progress)
        B) Structured JSON intake complete
    """
    
    prompt = f"""
    You are a medical intake receptionist.

    Your job is ONLY to collect structured intake information.
    You must NOT diagnose, triage, reassure, or give medical advice.

    You need to collect:
    1. Chief complaint (one main problem)
    2. Symptoms (list)
    3. Patient age
    4. Any known vitals (heart rate, SpO2) if volunteered

    Rules:
    - Ask ONE short question at a time
    - Ask ONLY for missing information
    - Be polite and neutral
    - When all required information is collected, return JSON ONLY
    - Do NOT include explanations if returning JSON

    Required final JSON format:
    {{
    "chiefComplaint": "",
    "symptoms": [],
    "vitals": {{
        "heartRate": null,
        "spo2": null
    }},
    "demographics": {{
        "age": null
    }}
    }}

    Conversation so far:
    {chat_history}
    """

    response = planner_llm(prompt)
    # print("LLM Response", response)

    # if model returned json, we assume intake is complete
    response = response.strip()
    if response.startswith("{"):
        try:
            # json.load() -> reads from a file, json.loads() -> read from a string
            parsed = json.loads(response)
            return {
                "status": "COMPLETE",
                "intake": normalize_intake(parsed)
            }
        except json.JSONDecodeError:
            return {
                "status": "IN_PROGRESS",
                "message": "Sorry, JSON parsing error. Could you please repeat ?"
            }
    
    # Otherwise LLM asks next quesion
    return {
        "status": "IN_PROGRESS",
        "message": response
    }
