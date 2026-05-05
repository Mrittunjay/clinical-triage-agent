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


**Steps to run the project:**
- Clone the repo main branch to PC
- Open the repo in VS Code or any other code editor of your choice (setps details is for VS Code if you are using different IDE the steps will be similar)
- Open the VS Code terminal, nevigate to he project folder and create a python virtual environment:
  python -m venv .venv  (.venv folder will be created inside your project folder)
- Activate the virtual environment by running the following command in your terminal:
  .\.venv\Scripts\activate
- Install requirements for the project:
  pip install -r requirements.txt
- To run the application server locally on your PC run the following command in the terminal.
  uvicorn app.main:app --reload
- Now to check the minimal Receptionist conversational intake agent open the following local host link in your suitable browser and start intake.
  http://127.0.0.1:8000/ui/intake.html
  <img width="543" height="414" alt="image" src="https://github.com/user-attachments/assets/7adfde05-0e46-49c1-bbaf-de42e23cbd8e" />
