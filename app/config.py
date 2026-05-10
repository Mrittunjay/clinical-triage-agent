from enum import Enum
from threading import Lock

class TriageStandard(str, Enum):
    NTS = "NTS"     # Netherlands Triage Standard
    ATP = "ATP"     # AIIMS Triage Protocol(Indian Triage Standard)

_config_lock = Lock()

TRIAGE_STANDARD = TriageStandard.ATP    # Default

def get_triage_standard() -> TriageStandard:
    with _config_lock:
        return TRIAGE_STANDARD
    
def set_triage_standard(value: str):
    global TRIAGE_STANDARD
    with _config_lock:
        TRIAGE_STANDARD = TriageStandard(value)
