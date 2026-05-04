from typing import List, Dict, TypedDict, Optional

# Intake content Schema for receptionist agent
class PatientIntake(TypedDict):
    """
    Intake structure expected by the Planner and Expert agent.
    TypedDict enforces structure creates a dictionary type such that a 
    type checker will expect all instances to have a certain set of keys, 
    where each key is associated with a value of a consistent type
    """
    chiefComplaint: str
    symptoms: List[str]
    vitals: Dict[str, Optional[float]]
    demographics: Dict[str, Optional[int]]
    intakeCompleteness: str
    missingFields: List[str]

