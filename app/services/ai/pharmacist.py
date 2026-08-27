MODEL_NAME = "iHIS Clinical Pharmacist Medication Safety Engine"
MODEL_VERSION = "1.0"


MEDICATION_SUGGESTIONS = {
    "Fever or mild pain": [
        "Paracetamol may be considered for fever or mild pain when clinically appropriate.",
    ],
    "Type 2 diabetes": [
        "Metformin is commonly considered in type 2 diabetes when clinically appropriate and not contraindicated.",
    ],
    "Suspected bacterial respiratory infection": [
        "Antibiotic therapy should only be considered when a bacterial infection is clinically suspected and selected according to allergy history and local antimicrobial guidance.",
    ],
    "Urinary tract infection": [
        "Antimicrobial treatment should be selected according to clinical assessment, allergy history, local resistance patterns, and culture results when available.",
    ],
}


INTERACTION_RULES = [
    {
        "drugs": {"warfarin", "ibuprofen"},
        "severity": "High",
        "message": (
            "Warfarin with ibuprofen may increase bleeding risk."
        ),
    },
    {
        "drugs": {"clarithromycin", "simvastatin"},
        "severity": "High",
        "message": (
            "Clarithromycin can substantially increase simvastatin exposure and toxicity risk."
        ),
    },
    {
        "drugs": {"warfarin", "aspirin"},
        "severity": "High",
        "message": (
            "Warfarin with aspirin may increase bleeding risk."
        ),
    },
    {
        "drugs": {"lisinopril", "spironolactone"},
        "severity": "Moderate",
        "message": (
            "Lisinopril with spironolactone may increase hyperkalemia risk."
        ),
    },
    {
        "drugs": {"metformin", "alcohol"},
        "severity": "Moderate",
        "message": (
            "Excessive alcohol use with metformin may increase metabolic complication risk."
        ),
    },
]


def normalize_medications(text):
    if not text:
        return []

    return [
        item.strip().lower()
        for item in text.split(",")
        if item.strip()
    ]


def check_interactions(medications):
    medication_set = set(medications)
    findings = []

    for rule in INTERACTION_RULES:
        if rule["drugs"].issubset(
            medication_set
        ):
            findings.append({
                "severity": rule["severity"],
                "drugs": sorted(
                    rule["drugs"]
                ),
                "message": rule["message"],
            })

    return findings


def check_contraindications(
    medications,
    allergies,
    renal_impairment,
):
    findings = []

    allergy_text = (
        allergies or ""
    ).lower()

    medication_set = set(
        medications
    )

    if (
        "penicillin" in allergy_text
        and (
            "amoxicillin" in medication_set
            or "ampicillin" in medication_set
        )
    ):
        findings.append(
            "Penicillin allergy recorded while a penicillin-class medication is listed."
        )

    if (
        renal_impairment
        and "metformin" in medication_set
    ):
        findings.append(
            "Renal impairment is recorded. Metformin requires renal-function assessment before use."
        )

    if (
        renal_impairment
        and (
            "ibuprofen" in medication_set
            or "diclofenac" in medication_set
        )
    ):
        findings.append(
            "Renal impairment is recorded with an NSAID. Renal risk should be reviewed."
        )

    return findings


def analyze_medication_safety(
    condition,
    current_medications,
    allergies,
    renal_impairment=False,
):
    medications = normalize_medications(
        current_medications
    )

    interactions = check_interactions(
        medications
    )

    contraindications = check_contraindications(
        medications,
        allergies,
        renal_impairment,
    )

    suggestions = MEDICATION_SUGGESTIONS.get(
        condition,
        [
            "Medication selection requires clinician assessment."
        ],
    )

    if contraindications:
        safety_status = "Contraindication / precaution detected"
    elif interactions:
        safety_status = "Interaction detected"
    else:
        safety_status = "No predefined safety alert detected"

    return {
        "condition": condition,
        "medications": medications,
        "suggestions": suggestions,
        "interactions": interactions,
        "contraindications": contraindications,
        "safety_status": safety_status,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "disclaimer": (
            "Educational medication-safety prototype only. "
            "Medication choice, dosing, interactions, and contraindications "
            "must be verified by a qualified healthcare professional and "
            "appropriate prescribing references."
        ),
    }
