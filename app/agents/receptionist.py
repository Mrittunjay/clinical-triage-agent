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