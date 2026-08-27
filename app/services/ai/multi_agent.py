from pathlib import Path

from app.services.ai.receptionist import route_patient
from app.services.ai.gp_disease import predict_gp_case
from app.services.ai.icu_cdss import analyze_icu_vitals
from app.services.ai.radiologist import analyze_xray
from app.services.ai.patient_education import answer_patient_question
from app.services.ai.pharmacist import analyze_medication_safety
from app.services.ai.mental_health import analyze_mental_health
from app.services.ai.clinical_reasoning import reason_from_symptoms
from app.services.ai.emergency_bfs import bfs_emergency_reasoning
from app.services.ai.oncology_dfs import dfs_oncology_reasoning
from app.services.ai.treatment_rl import optimize_treatment


ROOT = Path(__file__).resolve().parents[3]

DEMO_XRAY = (
    ROOT
    / "data"
    / "week4_demo"
    / "pneumonia.png"
)

SYSTEM_NAME = "iHIS Multi-Agent Clinical Orchestrator"
SYSTEM_VERSION = "1.0"


def run_integrated_case():
    communication_log = []

    receptionist = route_patient(
        "Fever, productive cough, fatigue and shortness of breath",
        "3 days",
    )

    communication_log.append(
        "Receptionist AI -> GP AI: "
        f"{receptionist['recommended_service']} / "
        f"{receptionist['urgency']}"
    )

    gp = predict_gp_case({
        "age": 55,
        "temperature": 38.8,
        "heart_rate": 108,
        "cough": True,
        "sputum": True,
        "dyspnea": True,
        "dysuria": False,
        "urinary_frequency": False,
        "abdominal_pain": False,
        "diarrhea": False,
        "vomiting": False,
        "smoking": True,
    })

    communication_log.append(
        "GP AI -> Clinical Reasoning AI: "
        f"{gp['predicted_condition']}"
    )

    icu = analyze_icu_vitals({
        "temperature": 38.8,
        "heart_rate": 108,
        "respiratory_rate": 22,
        "systolic_bp": 128,
        "oxygen_saturation": 95,
    })

    communication_log.append(
        "ICU AI -> Emergency AI: "
        f"status={icu['status']}"
    )

    if DEMO_XRAY.exists():
        radiology = analyze_xray(DEMO_XRAY)
    else:
        radiology = {
            "prediction": "Imaging unavailable",
            "interpretation": "Demonstration image not found.",
            "score": 0.0,
        }

    communication_log.append(
        "Radiologist AI -> Clinical Reasoning AI: "
        f"{radiology['prediction']}"
    )

    reasoning = reason_from_symptoms({
        "fever": True,
        "cough": True,
        "sputum": True,
        "dyspnea": True,
        "chest_pain": False,
        "sore_throat": False,
        "nasal_symptoms": False,
        "fatigue": True,
        "dysuria": False,
        "urinary_frequency": False,
        "lower_abdominal_pain": False,
        "abdominal_pain": False,
        "diarrhea": False,
        "vomiting": False,
        "nausea": False,
        "sweating": False,
        "wheeze": False,
        "chest_tightness": False,
    })

    communication_log.append(
        "Clinical Reasoning AI -> Patient Education AI: "
        f"{reasoning['leading_diagnosis']}"
    )

    emergency = bfs_emergency_reasoning({
        "chest_pain": False,
        "dyspnea": True,
        "sweating": False,
        "nausea": False,
        "tachycardia": True,
        "hemoptysis": False,
        "wheeze": False,
        "chest_tightness": False,
        "sudden_weakness": False,
        "speech_difficulty": False,
        "seizure": False,
        "altered_consciousness": False,
        "fever": True,
        "hypotension": False,
        "rash": False,
        "swelling": False,
    })

    education_question = (
        f"What should a patient know about "
        f"{gp['predicted_condition']}?"
    )

    education = answer_patient_question(
        education_question
    )

    communication_log.append(
        "GP AI -> Patient Education AI: "
        f"{education_question}"
    )

    pharmacy = analyze_medication_safety(
        condition="Suspected bacterial respiratory infection",
        current_medications="paracetamol",
        allergies="",
        renal_impairment=False,
    )

    communication_log.append(
        "GP AI -> Clinical Pharmacist AI: "
        "respiratory infection context"
    )

    mental_health = analyze_mental_health(
        0,
        0,
        1,
        0,
    )

    oncology = dfs_oncology_reasoning({
        "persistent_cough": True,
        "hemoptysis": False,
        "dyspnea": True,
        "chest_pain": False,
        "weight_loss": False,
        "smoking_history": True,
        "rectal_bleeding": False,
        "change_bowel_habit": False,
        "abdominal_pain": False,
        "anemia": False,
        "urinary_obstruction": False,
        "hematuria": False,
        "bone_pain": False,
        "elevated_psa": False,
    })

    treatment = optimize_treatment(
        "Localized",
        "0",
    )

    communication_log.append(
        "Oncologist AI -> Treatment Planning AI: "
        "Localized / ECOG 0"
    )

    integrated_summary = [
        f"Receptionist routing: {receptionist['recommended_service']} ({receptionist['urgency']}).",
        f"GP prediction: {gp['predicted_condition']} ({gp['confidence'] * 100:.1f}%).",
        f"ICU status: {icu['status']}.",
        f"Radiology result: {radiology['prediction']}.",
        f"Clinical reasoning: {reasoning['leading_diagnosis']}.",
        f"Emergency BFS triage: {emergency['triage']}.",
        f"Pharmacy safety: {pharmacy['safety_status']}.",
        f"Depression screen: {mental_health['depression_result']}.",
        f"Anxiety screen: {mental_health['anxiety_result']}.",
        f"Oncology DFS: {oncology['leading_pathway'] or 'No dominant pathway'}.",
        f"Treatment RL: {treatment['recommended_strategy']}.",
    ]

    return {
        "receptionist": receptionist,
        "gp": gp,
        "icu": icu,
        "radiology": radiology,
        "education": education,
        "pharmacy": pharmacy,
        "mental_health": mental_health,
        "reasoning": reasoning,
        "emergency": emergency,
        "oncology": oncology,
        "treatment": treatment,
        "communication_log": communication_log,
        "integrated_summary": integrated_summary,
        "system_name": SYSTEM_NAME,
        "system_version": SYSTEM_VERSION,
        "disclaimer": (
            "Educational multi-agent clinical decision-support "
            "prototype only. Not clinically validated."
        ),
    }
