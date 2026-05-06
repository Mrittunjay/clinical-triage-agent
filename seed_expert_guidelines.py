# Data ingestion mechanism for RAG expert agent
# Using official Azure AI Search SDK classes
import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
load_dotenv()

# Read environmental variables
SEARCH_ENDPOINT= os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX")

# Creating a search client
# This client directly talks to our index
# Same oject will later be used by the Expert Agent to retrieve docs
client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(SEARCH_KEY),
)

# Export guideline documents (authoritative, short, explicit)
# These are export facts, each document here encodes one decision rule,

# AIIMS TRIAGE PROTOCOL
ATP_DOCUMENTS = [
  {
    "id": "atp_airway_red_01",
    "standard": "ATP",
    "category": "Airway",
    "triageColor": "RED",
    "content": "Airway obstruction or imminent airway compromise requires immediate RED triage due to risk of hypoxia and respiratory failure.",
    "source": "AIIMS Triage Protocol (summarized)"
  },
  {
    "id": "atp_resp_distress_red_02",
    "standard": "ATP",
    "category": "Breathing",
    "triageColor": "RED",
    "content": "Severe respiratory distress with inability to speak full sentences indicates critical illness and requires RED triage.",
    "source": "AIIMS Emergency Care Principles"
  },
  {
    "id": "atp_spo2_low_red_03",
    "standard": "ATP",
    "category": "Vitals",
    "triageColor": "RED",
    "content": "Oxygen saturation below 94 percent in adults is considered hypoxia and mandates immediate RED triage.",
    "source": "AIIMS Respiratory Care Guidance"
  },
  {
    "id": "atp_chest_pain_red_04",
    "standard": "ATP",
    "category": "Cardiac",
    "triageColor": "RED",
    "content": "Chest pain suspected to be cardiac in origin, especially with breathlessness or diaphoresis, requires RED triage.",
    "source": "AIIMS Cardiac Emergency Protocol"
  },
  {
    "id": "atp_acute_dyspnea_red_05",
    "standard": "ATP",
    "category": "Breathing",
    "triageColor": "RED",
    "content": "Sudden onset breathlessness with hypoxia or respiratory fatigue is a life-threatening emergency requiring RED triage.",
    "source": "AIIMS Emergency Medicine SOP"
  },
  {
    "id": "atp_loc_red_06",
    "standard": "ATP",
    "category": "Neurology",
    "triageColor": "RED",
    "content": "Altered level of consciousness or unresponsiveness indicates severe neurological or metabolic pathology and requires RED triage.",
    "source": "AIIMS Neurological Emergencies"
  },
  {
    "id": "atp_seizure_red_07",
    "standard": "ATP",
    "category": "Neurology",
    "triageColor": "RED",
    "content": "Active seizures or status epilepticus require immediate RED triage to prevent neurological injury.",
    "source": "AIIMS Neurology Protocol"
  },
  {
    "id": "atp_stroke_red_08",
    "standard": "ATP",
    "category": "Neurology",
    "triageColor": "RED",
    "content": "New focal neurological deficits or suspected acute stroke warrant immediate RED triage for time-sensitive intervention.",
    "source": "AIIMS Stroke Pathway"
  },
  {
    "id": "atp_shock_red_09",
    "standard": "ATP",
    "category": "Circulation",
    "triageColor": "RED",
    "content": "Signs of shock including hypotension, tachycardia, or cold extremities require immediate RED triage.",
    "source": "AIIMS Shock Management"
  },
  {
    "id": "atp_sepsis_red_10",
    "standard": "ATP",
    "category": "Infection",
    "triageColor": "RED",
    "content": "Fever with hypotension or altered sensorium suggests sepsis and requires RED triage.",
    "source": "AIIMS Sepsis Protocol"
  },
  {
    "id": "atp_trauma_bleeding_red_11",
    "standard": "ATP",
    "category": "Trauma",
    "triageColor": "RED",
    "content": "Severe trauma with active or uncontrolled bleeding requires immediate RED triage.",
    "source": "AIIMS Trauma Care"
  },
  {
    "id": "atp_head_injury_red_12",
    "standard": "ATP",
    "category": "Trauma",
    "triageColor": "RED",
    "content": "Head injury associated with loss of consciousness or vomiting requires RED triage.",
    "source": "AIIMS Head Injury Protocol"
  },
  {
    "id": "atp_acute_abdomen_red_13",
    "standard": "ATP",
    "category": "Abdominal",
    "triageColor": "RED",
    "content": "Severe abdominal pain with guarding or rigidity suggests acute abdomen and requires RED triage.",
    "source": "AIIMS Surgical Emergencies"
  },
  {
    "id": "atp_anaphylaxis_red_14",
    "standard": "ATP",
    "category": "Allergy",
    "triageColor": "RED",
    "content": "Anaphylaxis or severe allergic reaction with airway or circulatory compromise requires RED triage.",
    "source": "AIIMS Allergy Protocol"
  },
  {
    "id": "atp_poisoning_red_15",
    "standard": "ATP",
    "category": "Toxicology",
    "triageColor": "RED",
    "content": "Poisoning or overdose with systemic symptoms or altered mental status requires RED triage.",
    "source": "AIIMS Toxicology"
  },
  {
    "id": "atp_moderate_breathless_yellow_16",
    "standard": "ATP",
    "category": "Breathing",
    "triageColor": "YELLOW",
    "content": "Moderate breathlessness with stable oxygen saturation requires YELLOW triage for urgent assessment.",
    "source": "AIIMS Triage Flow"
  },
  {
    "id": "atp_chest_pain_yellow_17",
    "standard": "ATP",
    "category": "Cardiac",
    "triageColor": "YELLOW",
    "content": "Chest pain without red-flag features and stable vitals should be triaged YELLOW.",
    "source": "AIIMS Cardiac Triage"
  },
  {
    "id": "atp_abd_pain_yellow_18",
    "standard": "ATP",
    "category": "Abdominal",
    "triageColor": "YELLOW",
    "content": "Abdominal pain without peritoneal signs or instability should be triaged YELLOW.",
    "source": "AIIMS Surgical Triage"
  },
  {
    "id": "atp_fever_yellow_19",
    "standard": "ATP",
    "category": "Infection",
    "triageColor": "YELLOW",
    "content": "Fever without shock or altered mental status requires YELLOW triage for same-day evaluation.",
    "source": "AIIMS Infection Triage"
  },
  {
    "id": "atp_trauma_yellow_20",
    "standard": "ATP",
    "category": "Trauma",
    "triageColor": "YELLOW",
    "content": "Moderate trauma without hemodynamic compromise should be triaged YELLOW.",
    "source": "AIIMS Trauma Triage"
  },
  {
    "id": "atp_headache_yellow_21",
    "standard": "ATP",
    "category": "Neurology",
    "triageColor": "YELLOW",
    "content": "Headache without neurological deficit or red flags should be triaged YELLOW.",
    "source": "AIIMS Neurology Guidance"
  },
  {
    "id": "atp_dehydration_yellow_22",
    "standard": "ATP",
    "category": "General",
    "triageColor": "YELLOW",
    "content": "Persistent vomiting or diarrhea with dehydration risk requires YELLOW triage.",
    "source": "AIIMS Medical Triage"
  },
  {
    "id": "atp_postictal_yellow_23",
    "standard": "ATP",
    "category": "Neurology",
    "triageColor": "YELLOW",
    "content": "Post-ictal state with stable vitals requires YELLOW triage and observation.",
    "source": "AIIMS Epilepsy Care"
  },
  {
    "id": "atp_pain_yellow_24",
    "standard": "ATP",
    "category": "Pain",
    "triageColor": "YELLOW",
    "content": "Severe pain with stable vital signs requires YELLOW triage for urgent management.",
    "source": "AIIMS Pain Management"
  },
  {
    "id": "atp_elderly_decline_yellow_25",
    "standard": "ATP",
    "category": "Geriatric",
    "triageColor": "YELLOW",
    "content": "Elderly patients with acute functional decline but stable vitals should be triaged YELLOW.",
    "source": "AIIMS Geriatric Care"
  },
  {
    "id": "atp_uri_green_26",
    "standard": "ATP",
    "category": "Respiratory",
    "triageColor": "GREEN",
    "content": "Mild upper respiratory symptoms with normal vital signs may be triaged GREEN.",
    "source": "AIIMS Outpatient Guidance"
  },
  {
    "id": "atp_minor_injury_green_27",
    "standard": "ATP",
    "category": "Trauma",
    "triageColor": "GREEN",
    "content": "Minor injuries without functional limitation may be triaged GREEN.",
    "source": "AIIMS Minor Injury Care"
  },
  {
    "id": "atp_chronic_green_28",
    "standard": "ATP",
    "category": "General",
    "triageColor": "GREEN",
    "content": "Stable chronic complaints without acute worsening may be triaged GREEN.",
    "source": "AIIMS OPD Triage"
  },
  {
    "id": "atp_followup_green_29",
    "standard": "ATP",
    "category": "General",
    "triageColor": "GREEN",
    "content": "Follow-up visits without new symptoms may be triaged GREEN.",
    "source": "AIIMS OPD Triage"
  },
  {
    "id": "atp_reassurance_green_30",
    "standard": "ATP",
    "category": "General",
    "triageColor": "GREEN",
    "content": "Mild symptoms requiring reassurance only may be triaged GREEN.",
    "source": "AIIMS Triage Flow"
  }
]

# NETHERLANDS TRIAGE STANDARD
NTS_DOCUMENTS = [
  {
    "id": "nts_airway_u1_01",
    "standard": "NTS",
    "category": "Airway",
    "triageColor": "RED",
    "content": "Airway compromise or obstruction is classified as U1 urgency under the Netherlands Triage Standard.",
    "source": "Netherlands Triage Standard (summarized)"
  },
  {
    "id": "nts_severe_dyspnea_u1_02",
    "standard": "NTS",
    "category": "Breathing",
    "triageColor": "RED",
    "content": "Severe dyspnea with signs of fatigue or cyanosis corresponds to U1 urgency under NTS.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_cyanosis_u1_03",
    "standard": "NTS",
    "category": "Breathing",
    "triageColor": "RED",
    "content": "Cyanosis or critically low oxygenation is triaged as U1 urgency under NTS.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_chest_pain_u1_04",
    "standard": "NTS",
    "category": "Cardiac",
    "triageColor": "RED",
    "content": "Thoracic pain suspected of cardiac origin with acute symptoms is classified as U1 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_neuro_deficit_u1_05",
    "standard": "NTS",
    "category": "Neurology",
    "triageColor": "RED",
    "content": "Sudden neurological deficits or reduced consciousness require U1 urgency under NTS.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_seizure_u1_06",
    "standard": "NTS",
    "category": "Neurology",
    "triageColor": "RED",
    "content": "Active seizures or prolonged post-ictal unresponsiveness are classified as U1 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_shock_u1_07",
    "standard": "NTS",
    "category": "Circulation",
    "triageColor": "RED",
    "content": "Hemodynamic instability or shock requires immediate U1 triage under NTS.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_trauma_u1_08",
    "standard": "NTS",
    "category": "Trauma",
    "triageColor": "RED",
    "content": "High-risk trauma presentations per NTS criteria are triaged as U1 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_stroke_u1_09",
    "standard": "NTS",
    "category": "Neurology",
    "triageColor": "RED",
    "content": "Suspected acute stroke is classified as U1 urgency to enable time-critical treatment.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_acute_abdomen_u1_10",
    "standard": "NTS",
    "category": "Abdominal",
    "triageColor": "RED",
    "content": "Severe abdominal pain with suspected acute abdomen is triaged as U1 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_anaphylaxis_u1_11",
    "standard": "NTS",
    "category": "Allergy",
    "triageColor": "RED",
    "content": "Anaphylaxis or severe allergic response requires U1 urgency under NTS.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_pediatric_distress_u1_12",
    "standard": "NTS",
    "category": "Pediatrics",
    "triageColor": "RED",
    "content": "Pediatric acute distress, lethargy, or poor perfusion are classified as U1 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_fever_instability_u1_13",
    "standard": "NTS",
    "category": "Infection",
    "triageColor": "RED",
    "content": "High fever with systemic instability is triaged as U1 urgency under NTS.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_bleeding_u1_14",
    "standard": "NTS",
    "category": "Trauma",
    "triageColor": "RED",
    "content": "Uncontrolled external bleeding requires immediate U1 triage.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_intoxication_u1_15",
    "standard": "NTS",
    "category": "Toxicology",
    "triageColor": "RED",
    "content": "Intoxication with altered mental status or instability is classified as U1 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_dyspnea_u3_16",
    "standard": "NTS",
    "category": "Breathing",
    "triageColor": "YELLOW",
    "content": "Moderate dyspnea with stable oxygenation should be triaged as U3 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_chest_pain_u3_17",
    "standard": "NTS",
    "category": "Cardiac",
    "triageColor": "YELLOW",
    "content": "Chest pain without immediate cardiac suspicion is classified as U3 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_abd_pain_u3_18",
    "standard": "NTS",
    "category": "Abdominal",
    "triageColor": "YELLOW",
    "content": "Abdominal pain without guarding or shock may be triaged as U3 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_fever_u3_19",
    "standard": "NTS",
    "category": "Infection",
    "triageColor": "YELLOW",
    "content": "Fever requiring same-day medical assessment corresponds to U3 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_trauma_u3_20",
    "standard": "NTS",
    "category": "Trauma",
    "triageColor": "YELLOW",
    "content": "Moderate trauma without physiological instability is classified as U3 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_headache_u3_21",
    "standard": "NTS",
    "category": "Neurology",
    "triageColor": "YELLOW",
    "content": "Headache without red-flag neurological signs is typically U3 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_dehydration_u3_22",
    "standard": "NTS",
    "category": "General",
    "triageColor": "YELLOW",
    "content": "Persistent vomiting or dehydration risk qualifies for U3 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_infection_u3_23",
    "standard": "NTS",
    "category": "Infection",
    "triageColor": "YELLOW",
    "content": "Acute infections requiring urgent review are triaged as U3.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_functional_impairment_u3_24",
    "standard": "NTS",
    "category": "General",
    "triageColor": "YELLOW",
    "content": "Significant functional impairment without instability is classified as U3 urgency.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_elderly_u3_25",
    "standard": "NTS",
    "category": "Geriatric",
    "triageColor": "YELLOW",
    "content": "Elderly patients with new symptoms and stable vitals are commonly triaged U3.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_uri_u5_26",
    "standard": "NTS",
    "category": "Respiratory",
    "triageColor": "GREEN",
    "content": "Mild respiratory or ENT complaints without red flags may be triaged as U4 or U5.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_minor_wound_u5_27",
    "standard": "NTS",
    "category": "Trauma",
    "triageColor": "GREEN",
    "content": "Minor wounds or superficial injuries are generally classified as U5 under NTS.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_msk_pain_u5_28",
    "standard": "NTS",
    "category": "Musculoskeletal",
    "triageColor": "GREEN",
    "content": "Stable musculoskeletal pain without red flags may be triaged as U4 or U5.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_chronic_u5_29",
    "standard": "NTS",
    "category": "General",
    "triageColor": "GREEN",
    "content": "Chronic complaints without acute deterioration are triaged as U4 or U5.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_advice_u5_30",
    "standard": "NTS",
    "category": "General",
    "triageColor": "GREEN",
    "content": "Administrative, advice-only, or reassurance-only presentations are classified as U5.",
    "source": "Netherlands Triage Standard"
  }
]

# Combining the ATP and NTS triage protocols beforing pushing into clinical expert search index.
documents = ATP_DOCUMENTS + NTS_DOCUMENTS

# Upload documents to Azure AI search -> Calls Azure Search indexing API
# Azure then handles batching, validation and storage
result = client.upload_documents(documents)

# Print upload status 
for r in result:
    print(f"Document {r.key} uploaded: {r.succeeded}")

# Run this script in terminal for data ingestion.
