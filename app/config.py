import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class TriageStandard(str, Enum):
    NTS = "NTS"     # Netherlands Triage Standard
    ITS = "ATP"     # AIIMS Triage Protocol(Indian Triage Standard)

# Read from environment variable
TRIAGE_STANDARD = TriageStandard(
    os.getenv("TRIAGE_STANDARD", "ATP")     # default to ATP
)