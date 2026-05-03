**Multi Agent Patient Triage and Care Coordination**

**Overview**

This project implements a multi‑agent clinical triage assistant designed to support medical professionals during the emergency triage process.
The system follows a human‑in‑the‑loop approach:

- AI agents assist with intake, triage reasoning, and clinical suggestions
- Human clinicians remain the final decision makers

At this stage, the project focuses on intake, triage reasoning, expert guideline validation (RAG), and decision recording.
The project is still under construction...


**Current High Level Architecture**

The system has specialized agents, each with a clear responsibility:

- Receptionist Agent – Patient intake & normalization
- Planner Agent – Orchestrates workflow and reasoning
- Expert Agent (RAG + Rules) – Clinical triage authority
- Librarian Agent (FHIR) – Patient history and record management
- Content Safety Service – Safety review of text inputs
- Human Clinician – Observes, verifies, and makes final decisions

**Current Code Structure**

app/

├── agents/

│   ├── receptionist.py      # Intake normalization

│   ├── expert_rag.py        # Expert triage (RAG + rules)

│   └── librarian_fhir.py    # Patient history & record persistence

│

├── services/

│   ├── openai_client.py     # Azure OpenAI wrapper

│   ├── content_safety.py    # Azure Content Safety

│   └── ai_search_client.py  # Azure AI Search helpers

│

├── planner.py               # Workflow orchestration

├── main.py                  # FastAPI entry point

└── models.py                # Shared data models
