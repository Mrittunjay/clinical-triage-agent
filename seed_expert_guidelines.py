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
    "content": (
      "Airway obstruction or imminent airway compromise requires immediate RED triage due to risk of hypoxia and respiratory failure. "
      "Recommended tests and immediate assessments include airway patency assessment, pulse oximetry, arterial blood gas if available, "
      "and preparation for definitive airway management."
    ),
    "source": "AIIMS Triage Protocol (summarized)"
  },
  {
    "id": "atp_resp_distress_red_02",
    "standard": "ATP",
    "category": "Breathing",
    "triageColor": "RED",
    "content": (
      "Severe respiratory distress with inability to speak full sentences indicates critical illness and requires RED triage. "
      "Recommended tests include pulse oximetry, arterial blood gas, chest X-ray, and ECG if a cardiopulmonary cause is suspected."
    ),
    "source": "AIIMS Emergency Care Principles"
  },
  {
    "id": "atp_spo2_low_red_03",
    "standard": "ATP",
    "category": "Vitals",
    "triageColor": "RED",
    "content": (
      "Oxygen saturation below 94 percent in adults is considered hypoxia and mandates immediate RED triage. "
      "Recommended tests include repeat pulse oximetry, arterial blood gas analysis, and chest imaging as clinically indicated."
    ),
    "source": "AIIMS Respiratory Care Guidance"
  },
  {
    "id": "atp_chest_pain_red_04",
    "standard": "ATP",
    "category": "Cardiac",
    "triageColor": "RED",
    "content": (
      "Chest pain suspected to be cardiac in origin, especially with breathlessness or diaphoresis, requires RED triage. "
      "Recommended tests include ECG, cardiac biomarkers such as troponin, chest X-ray, and continuous cardiac monitoring."
    ),
    "source": "AIIMS Cardiac Emergency Protocol"
  },
  {
    "id": "atp_acute_dyspnea_red_05",
    "standard": "ATP",
    "category": "Breathing",
    "triageColor": "RED",
    "content": (
      "Sudden onset breathlessness with hypoxia or respiratory fatigue is a life-threatening emergency requiring RED triage. "
      "Recommended tests include pulse oximetry, arterial blood gas, chest X-ray, and ECG."
    ),
    "source": "AIIMS Emergency Medicine SOP"
  },
  {
    "id": "atp_loc_red_06",
    "standard": "ATP",
    "category": "Neurology",
    "triageColor": "RED",
    "content": (
      "Altered level of consciousness or unresponsiveness indicates severe neurological or metabolic pathology and requires RED triage. "
      "Recommended tests include capillary blood glucose, serum electrolytes, arterial blood gas, and neuroimaging as indicated."
    ),
    "source": "AIIMS Neurological Emergencies"
  },
  {
    "id": "atp_seizure_red_07",
    "standard": "ATP",
    "category": "Neurology",
    "triageColor": "RED",
    "content": (
      "Active seizures or status epilepticus require immediate RED triage to prevent neurological injury. "
      "Recommended tests include blood glucose estimation, serum electrolytes, anticonvulsant drug levels when applicable, "
      "and EEG or neuroimaging as clinically indicated."
    ),
    "source": "AIIMS Neurology Protocol"
  },
  {
    "id": "atp_stroke_red_08",
    "standard": "ATP",
    "category": "Neurology",
    "triageColor": "RED",
    "content": (
      "New focal neurological deficits or suspected acute stroke warrant immediate RED triage for time-sensitive intervention. "
      "Recommended tests include immediate blood glucose check, non-contrast CT brain, ECG, and basic blood investigations."
    ),
    "source": "AIIMS Stroke Pathway"
  },
  {
    "id": "atp_shock_red_09",
    "standard": "ATP",
    "category": "Circulation",
    "triageColor": "RED",
    "content": (
      "Signs of shock including hypotension, tachycardia, or cold extremities require immediate RED triage. "
      "Recommended tests include blood pressure monitoring, complete blood count, serum lactate, arterial blood gas, and ECG."
    ),
    "source": "AIIMS Shock Management"
  },
  {
    "id": "atp_sepsis_red_10",
    "standard": "ATP",
    "category": "Infection",
    "triageColor": "RED",
    "content": (
      "Fever with hypotension or altered sensorium suggests sepsis and requires RED triage. "
      "Recommended tests include complete blood count, blood cultures, serum lactate, renal function tests, and chest X-ray."
    ),
    "source": "AIIMS Sepsis Protocol"
  },
  {
    "id": "atp_trauma_bleeding_red_11",
    "standard": "ATP",
    "category": "Trauma",
    "triageColor": "RED",
    "content": (
      "Severe trauma with active or uncontrolled bleeding requires immediate RED triage. "
      "Recommended tests include complete blood count, blood grouping and cross-match, FAST ultrasound, and CT imaging as indicated."
    ),
    "source": "AIIMS Trauma Care"
  },
  {
    "id": "atp_head_injury_red_12",
    "standard": "ATP",
    "category": "Trauma",
    "triageColor": "RED",
    "content": (
      "Head injury associated with loss of consciousness or vomiting requires RED triage. "
      "Recommended tests include Glasgow Coma Scale assessment, CT scan of the brain, and cervical spine evaluation."
    ),
    "source": "AIIMS Head Injury Protocol"
  },
  {
    "id": "atp_acute_abdomen_red_13",
    "standard": "ATP",
    "category": "Abdominal",
    "triageColor": "RED",
    "content": (
      "Severe abdominal pain with guarding or rigidity suggests acute abdomen and requires RED triage. "
      "Recommended tests include complete blood count, serum electrolytes, liver function tests, serum amylase or lipase, "
      "and abdominal ultrasound or CT scan as indicated."
    ),
    "source": "AIIMS Surgical Emergencies"
  },
  {
    "id": "atp_anaphylaxis_red_14",
    "standard": "ATP",
    "category": "Allergy",
    "triageColor": "RED",
    "content": (
      "Anaphylaxis or severe allergic reaction with airway or circulatory compromise requires RED triage. "
      "Recommended assessments include airway and hemodynamic monitoring; laboratory tests are secondary to immediate treatment."
    ),
    "source": "AIIMS Allergy Protocol"
  },
  {
    "id": "atp_poisoning_red_15",
    "standard": "ATP",
    "category": "Toxicology",
    "triageColor": "RED",
    "content": (
      "Poisoning or overdose with systemic symptoms or altered mental status requires RED triage. "
      "Recommended tests include blood glucose, arterial blood gas, serum electrolytes, toxicology screening, and ECG."
    ),
    "source": "AIIMS Toxicology"
  },
  {
    "id": "atp_moderate_breathless_yellow_16",
    "standard": "ATP",
    "category": "Breathing",
    "triageColor": "YELLOW",
    "content": (
      "Moderate breathlessness with stable oxygen saturation requires YELLOW triage for urgent assessment. "
      "Recommended tests include pulse oximetry, chest X-ray, and ECG if clinically indicated."
    ),
    "source": "AIIMS Triage Flow"
  },
  {
    "id": "atp_chest_pain_yellow_17",
    "standard": "ATP",
    "category": "Cardiac",
    "triageColor": "YELLOW",
    "content": (
      "Chest pain without red-flag features and stable vitals should be triaged YELLOW. "
      "Recommended tests include ECG and cardiac biomarkers for risk stratification."
    ),
    "source": "AIIMS Cardiac Triage"
  },
  {
    "id": "atp_abd_pain_yellow_18",
    "standard": "ATP",
    "category": "Abdominal",
    "triageColor": "YELLOW",
    "content": (
      "Abdominal pain without peritoneal signs or instability should be triaged YELLOW. "
      "Recommended tests include complete blood count, urine routine examination, and abdominal ultrasound if symptoms persist."
    ),
    "source": "AIIMS Surgical Triage"
  },
  {
    "id": "atp_fever_yellow_19",
    "standard": "ATP",
    "category": "Infection",
    "triageColor": "YELLOW",
    "content": (
      "Fever without shock or altered mental status requires YELLOW triage for same-day evaluation. "
      "Recommended tests include complete blood count, urine routine examination, and chest X-ray as indicated."
    ),
    "source": "AIIMS Infection Triage"
  },
  {
    "id": "atp_trauma_yellow_20",
    "standard": "ATP",
    "category": "Trauma",
    "triageColor": "YELLOW",
    "content": (
      "Moderate trauma without hemodynamic compromise should be triaged YELLOW. "
      "Recommended tests include complete blood count and appropriate imaging based on injury pattern."
    ),
    "source": "AIIMS Trauma Triage"
  },
  {
    "id": "atp_headache_yellow_21",
    "standard": "ATP",
    "category": "Neurology",
    "triageColor": "YELLOW",
    "content": (
      "Headache without neurological deficit or red flags should be triaged YELLOW. "
      "Recommended tests include blood pressure measurement and basic neurological assessment; "
      "neuroimaging if red flags develop."
    ),
    "source": "AIIMS Neurology Guidance"
  },
  {
    "id": "atp_dehydration_yellow_22",
    "standard": "ATP",
    "category": "General",
    "triageColor": "YELLOW",
    "content": (
      "Persistent vomiting or diarrhea with dehydration risk requires YELLOW triage. "
      "Recommended tests include serum electrolytes, blood urea, creatinine, and urine output assessment."
    ),
    "source": "AIIMS Medical Triage"
  },
  {
    "id": "atp_postictal_yellow_23",
    "standard": "ATP",
    "category": "Neurology",
    "triageColor": "YELLOW",
    "content": (
      "Post-ictal state with stable vitals requires YELLOW triage and observation. "
      "Recommended tests include blood glucose and serum electrolytes."
    ),
    "source": "AIIMS Epilepsy Care"
  },
  {
    "id": "atp_pain_yellow_24",
    "standard": "ATP",
    "category": "Pain",
    "triageColor": "YELLOW",
    "content": (
      "Severe pain with stable vital signs requires YELLOW triage for urgent management. "
      "Recommended tests are guided by the pain site and may include basic blood investigations and imaging."
    ),
    "source": "AIIMS Pain Management"
  },
  {
    "id": "atp_elderly_decline_yellow_25",
    "standard": "ATP",
    "category": "Geriatric",
    "triageColor": "YELLOW",
    "content": (
      "Elderly patients with acute functional decline but stable vitals should be triaged YELLOW. "
      "Recommended tests include complete blood count, serum electrolytes, renal function tests, and urine examination."
    ),
    "source": "AIIMS Geriatric Care"
  },
  {
    "id": "atp_uri_green_26",
    "standard": "ATP",
    "category": "Respiratory",
    "triageColor": "GREEN",
    "content": (
      "Mild upper respiratory symptoms with normal vital signs may be triaged GREEN. "
      "Recommended tests are usually not required unless symptoms persist or worsen."
    ),
    "source": "AIIMS Outpatient Guidance"
  },
  {
    "id": "atp_minor_injury_green_27",
    "standard": "ATP",
    "category": "Trauma",
    "triageColor": "GREEN",
    "content": (
      "Minor injuries without functional limitation may be triaged GREEN. "
      "Recommended tests are generally not necessary; local examination is sufficient."
    ),
    "source": "AIIMS Minor Injury Care"
  },
  {
    "id": "atp_chronic_green_28",
    "standard": "ATP",
    "category": "General",
    "triageColor": "GREEN",
    "content": (
      "Stable chronic complaints without acute worsening may be triaged GREEN. "
      "Recommended tests are not required during triage."
    ),
    "source": "AIIMS OPD Triage"
  },
  {
    "id": "atp_followup_green_29",
    "standard": "ATP",
    "category": "General",
    "triageColor": "GREEN",
    "content": (
      "Follow-up visits without new symptoms may be triaged GREEN. "
      "Recommended tests are as per existing treatment plan."
    ),
    "source": "AIIMS OPD Triage"
  },
  {
    "id": "atp_reassurance_green_30",
    "standard": "ATP",
    "category": "General",
    "triageColor": "GREEN",
    "content": (
      "Mild symptoms requiring reassurance only may be triaged GREEN. "
      "No investigations are required at triage."
    ),
    "source": "AIIMS Triage Flow"
  },
  {
    "id": "atp_eye_pain_yellow_31",
    "standard": "ATP",
    "category": "Opthalmology",
    "triageColor": "YELLOW",
    "content": (
      "Eye pain with redness, irritation, or foreign body sensation without vision loss, trauma, or neurological deficits "
      "should be triaged YELLOW. Recommended tests include visual acuity assessment and slit-lamp examination."
    ),
    "source": "AIIMS Opthalmology Emergency Guidelines"
  },
  {
    "id": "atp_limb_pain_yellow_32",
    "standard": "ATP",
    "category": "Musculoskeletal",
    "triageColor": "YELLOW",
    "content": (
      "Limb pain without deformity, neurovascular compromise, severe trauma, or systemic instability should be triaged YELLOW. "
      "Recommended tests include local examination and X-ray if fracture is suspected."
    ),
    "source": "AIIMS Orthopaedic Emergency Guidelines"
  },
  {
    "id": "atp_neck_swelling_airway_red_33",
    "standard": "ATP",
    "category": "Airway",
    "triageColor": "RED",
    "content": (
      "Neck or throat swelling with potential airway compromise, difficulty swallowing, or hypoxia requires immediate RED triage. "
      "Recommended tests include airway assessment, pulse oximetry, and imaging of the neck if clinically feasible."
    ),
    "source": "AIIMS Airway Emergency Guidelines"
  },
  {
    "id": "atp_gastro_loose_motion_yellow_34",
    "standard": "ATP",
    "category": "Gastrointestinal",
    "triageColor": "YELLOW",
    "content": (
      "Stomach or abdominal pain associated with loose motions, without severe dehydration, shock, blood in stools, or altered mental status, "
      "should be triaged YELLOW. Recommended tests include stool examination, serum electrolytes, complete blood count, and hydration assessment."
    ),
    "source": "AIIMS Gastrointestinal Triage Guidance"
  }
]


# NETHERLANDS TRIAGE STANDARD
NTS_DOCUMENTS = [
  {
    "id": "nts_airway_u1_01",
    "standard": "NTS",
    "category": "Airway",
    "triageColor": "RED",
    "content": "Airway compromise or obstruction is classified as U1 urgency under the Netherlands Triage Standard. Recommended tests include airway assessment, pulse oximetry, and arterial blood gas if available.",
    "source": "Netherlands Triage Standard (summarized)"
  },
  {
    "id": "nts_severe_dyspnea_u1_02",
    "standard": "NTS",
    "category": "Breathing",
    "triageColor": "RED",
    "content": "Severe dyspnea with signs of fatigue or cyanosis corresponds to U1 urgency under NTS. Recommended tests include pulse oximetry, arterial blood gas, chest X-ray, and ECG.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_cyanosis_u1_03",
    "standard": "NTS",
    "category": "Breathing",
    "triageColor": "RED",
    "content": "Cyanosis or critically low oxygenation is triaged as U1 urgency under NTS. Recommended tests include pulse oximetry, arterial blood gas, and chest imaging.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_chest_pain_u1_04",
    "standard": "NTS",
    "category": "Cardiac",
    "triageColor": "RED",
    "content": "Thoracic pain suspected of cardiac origin with acute symptoms is classified as U1 urgency. Recommended tests include ECG, cardiac biomarkers, and chest X-ray.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_neuro_deficit_u1_05",
    "standard": "NTS",
    "category": "Neurology",
    "triageColor": "RED",
    "content": "Sudden neurological deficits or reduced consciousness require U1 urgency under NTS. Recommended tests include blood glucose, CT brain, and basic blood investigations.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_seizure_u1_06",
    "standard": "NTS",
    "category": "Neurology",
    "triageColor": "RED",
    "content": "Active seizures or prolonged post-ictal unresponsiveness are classified as U1 urgency. Recommended tests include blood glucose, serum electrolytes, and EEG or neuroimaging as indicated.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_shock_u1_07",
    "standard": "NTS",
    "category": "Circulation",
    "triageColor": "RED",
    "content": "Hemodynamic instability or shock requires immediate U1 triage under NTS. Recommended tests include blood pressure monitoring, complete blood count, serum lactate, arterial blood gas, and ECG.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_trauma_u1_08",
    "standard": "NTS",
    "category": "Trauma",
    "triageColor": "RED",
    "content": "High-risk trauma presentations per NTS criteria are triaged as U1 urgency. Recommended tests include complete blood count, FAST ultrasound, and CT imaging as indicated.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_stroke_u1_09",
    "standard": "NTS",
    "category": "Neurology",
    "triageColor": "RED",
    "content": "Suspected acute stroke is classified as U1 urgency to enable time-critical treatment. Recommended tests include blood glucose measurement and non-contrast CT brain.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_acute_abdomen_u1_10",
    "standard": "NTS",
    "category": "Abdominal",
    "triageColor": "RED",
    "content": "Severe abdominal pain with suspected acute abdomen is triaged as U1 urgency. Recommended tests include complete blood count, serum electrolytes, and abdominal imaging.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_anaphylaxis_u1_11",
    "standard": "NTS",
    "category": "Allergy",
    "triageColor": "RED",
    "content": "Anaphylaxis or severe allergic response requires U1 urgency under NTS. Recommended assessments include airway and hemodynamic monitoring; laboratory tests are secondary.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_pediatric_distress_u1_12",
    "standard": "NTS",
    "category": "Pediatrics",
    "triageColor": "RED",
    "content": "Pediatric acute distress, lethargy, or poor perfusion are classified as U1 urgency. Recommended tests include blood glucose, venous blood gas, and basic blood investigations.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_fever_instability_u1_13",
    "standard": "NTS",
    "category": "Infection",
    "triageColor": "RED",
    "content": "High fever with systemic instability is triaged as U1 urgency under NTS. Recommended tests include complete blood count, blood cultures, serum lactate, and chest X-ray.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_bleeding_u1_14",
    "standard": "NTS",
    "category": "Trauma",
    "triageColor": "RED",
    "content": "Uncontrolled external bleeding requires immediate U1 triage. Recommended tests include complete blood count and blood grouping and cross-match.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_intoxication_u1_15",
    "standard": "NTS",
    "category": "Toxicology",
    "triageColor": "RED",
    "content": "Intoxication with altered mental status or instability is classified as U1 urgency. Recommended tests include blood glucose, arterial blood gas, serum electrolytes, and ECG.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_dyspnea_u3_16",
    "standard": "NTS",
    "category": "Breathing",
    "triageColor": "YELLOW",
    "content": "Moderate dyspnea with stable oxygenation should be triaged as U3 urgency. Recommended tests include pulse oximetry and chest X-ray.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_chest_pain_u3_17",
    "standard": "NTS",
    "category": "Cardiac",
    "triageColor": "YELLOW",
    "content": "Chest pain without immediate cardiac suspicion is classified as U3 urgency. Recommended tests include ECG and cardiac biomarkers for risk stratification.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_abd_pain_u3_18",
    "standard": "NTS",
    "category": "Abdominal",
    "triageColor": "YELLOW",
    "content": "Abdominal pain without guarding or shock may be triaged as U3 urgency. Recommended tests include complete blood count, urine examination, and abdominal ultrasound.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_fever_u3_19",
    "standard": "NTS",
    "category": "Infection",
    "triageColor": "YELLOW",
    "content": "Fever requiring same-day medical assessment corresponds to U3 urgency. Recommended tests include complete blood count and urine routine examination.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_trauma_u3_20",
    "standard": "NTS",
    "category": "Trauma",
    "triageColor": "YELLOW",
    "content": "Moderate trauma without physiological instability is classified as U3 urgency. Recommended tests include complete blood count and imaging as indicated.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_headache_u3_21",
    "standard": "NTS",
    "category": "Neurology",
    "triageColor": "YELLOW",
    "content": "Headache without red-flag neurological signs is typically U3 urgency. Recommended tests include blood pressure measurement and neurological examination.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_dehydration_u3_22",
    "standard": "NTS",
    "category": "General",
    "triageColor": "YELLOW",
    "content": "Persistent vomiting or dehydration risk qualifies for U3 urgency. Recommended tests include serum electrolytes, urea, creatinine, and hydration assessment.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_infection_u3_23",
    "standard": "NTS",
    "category": "Infection",
    "triageColor": "YELLOW",
    "content": "Acute infections requiring urgent review are triaged as U3. Recommended tests include complete blood count and infection-focused investigations.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_functional_impairment_u3_24",
    "standard": "NTS",
    "category": "General",
    "triageColor": "YELLOW",
    "content": "Significant functional impairment without instability is classified as U3 urgency. Recommended tests are guided by clinical presentation.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_elderly_u3_25",
    "standard": "NTS",
    "category": "Geriatric",
    "triageColor": "YELLOW",
    "content": "Elderly patients with new symptoms and stable vitals are commonly triaged U3. Recommended tests include complete blood count, serum electrolytes, and urine examination.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_uri_u5_26",
    "standard": "NTS",
    "category": "Respiratory",
    "triageColor": "GREEN",
    "content": "Mild respiratory or ENT complaints without red flags may be triaged as U4 or U5. Recommended tests are usually not required.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_minor_wound_u5_27",
    "standard": "NTS",
    "category": "Trauma",
    "triageColor": "GREEN",
    "content": "Minor wounds or superficial injuries are generally classified as U5 under NTS. Recommended tests are not required.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_msk_pain_u5_28",
    "standard": "NTS",
    "category": "Musculoskeletal",
    "triageColor": "GREEN",
    "content": "Stable musculoskeletal pain without red flags may be triaged as U4 or U5. Recommended tests are not required at triage.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_chronic_u5_29",
    "standard": "NTS",
    "category": "General",
    "triageColor": "GREEN",
    "content": "Chronic complaints without acute deterioration are triaged as U4 or U5. No investigations are required at triage.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_advice_u5_30",
    "standard": "NTS",
    "category": "General",
    "triageColor": "GREEN",
    "content": "Administrative, advice-only, or reassurance-only presentations are classified as U5. No investigations are required.",
    "source": "Netherlands Triage Standard"
  },
  {
    "id": "nts_eye_pain_u3_31",
    "standard": "NTS",
    "category": "Ophthalmology",
    "triageColor": "YELLOW",
    "content": "Eye pain with redness or irritation without vision loss, trauma, or severe systemic symptoms is classified as U3 urgency under NTS. Recommended tests include visual acuity assessment.",
    "source": "Netherlands Triage Standard - Eye Complaints"
  },
  {
    "id": "nts_limb_pain_u3_32",
    "standard": "NTS",
    "category": "Musculoskeletal",
    "triageColor": "YELLOW",
    "content": "Limb pain without deformity, circulatory compromise, or neurological deficit is classified as U3 urgency under NTS. Recommended tests include local examination and X-ray if indicated.",
    "source": "Netherlands Triage Standard - Musculoskeletal Complaints"
  },
  {
    "id": "nts_neck_swelling_u1_33",
    "standard": "NTS",
    "category": "Airway",
    "triageColor": "RED",
    "content": "Neck or throat swelling with potential airway compromise, stridor, dysphagia, or hypoxia is classified as U1 urgency under NTS. Recommended tests include airway assessment and pulse oximetry.",
    "source": "Netherlands Triage Standard - Airway Emergencies"
  },
  {
    "id": "nts_gastro_loose_motion_u3_34",
    "standard": "NTS",
    "category": "Gastrointestinal",
    "triageColor": "YELLOW",
    "content": "Abdominal pain with loose motions without dehydration, shock, blood in stools, or altered mental status is classified as U3 urgency under NTS. Recommended tests include stool examination, serum electrolytes, and complete blood count.",
    "source": "Netherlands Triage Standard - Gastrointestinal Complaints"
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
