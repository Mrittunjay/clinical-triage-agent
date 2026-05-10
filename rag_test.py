from app.services.ai_search_client import AISearchClient

client = AISearchClient()

intake = {
    'chiefComplaint': 'neck pain', 
    'symptoms': ['swollen throat'], 
    'vitals': {'heartRate': 88, 'spo2': 99}, 
    'demographics': {'age': 44}
}

docs = client.retrieve_guidelines(intake)