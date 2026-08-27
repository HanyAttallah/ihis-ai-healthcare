MODEL_NAME = "iHIS Clinical Reasoning Engine"
MODEL_VERSION = "1.0"


DISEASE_RULES = {
    "Pneumonia": {
        "fever": 2,
        "cough": 3,
        "sputum": 2,
        "dyspnea": 2,
        "chest_pain": 1,
    },
    "Upper respiratory infection": {
        "fever": 1,
        "cough": 3,
        "sore_throat": 3,
        "nasal_symptoms": 2,
        "fatigue": 1,
    },
    "Urinary tract infection": {
        "fever": 1,
        "dysuria": 4,
        "urinary_frequency": 4,
        "lower_abdominal_pain": 2,
    },
    "Gastroenteritis": {
        "fever": 1,
        "abdominal_pain": 2,
        "diarrhea": 4,
        "vomiting": 3,
        "nausea": 2,
    },
    "Acute coronary syndrome": {
        "chest_pain": 5,
        "dyspnea": 2,
        "sweating": 2,
        "nausea": 1,
    },
    "Asthma exacerbation": {
        "dyspnea": 4,
        "wheeze": 5,
        "cough": 2,
        "chest_tightness": 3,
    },
}


EXPLANATIONS = {
    "Pneumonia": (
        "Pneumonia is considered when respiratory symptoms such as cough, "
        "sputum production, fever, and dyspnea occur together."
    ),
    "Upper respiratory infection": (
        "Upper respiratory infection is considered when cough, sore throat, "
        "nasal symptoms, fever, and fatigue occur without stronger evidence "
        "for lower respiratory disease."
    ),
    "Urinary tract infection": (
        "Urinary tract infection is supported by dysuria, urinary frequency, "
        "lower abdominal discomfort, and sometimes fever."
    ),
    "Gastroenteritis": (
        "Gastroenteritis is supported by diarrhea, vomiting, nausea, "
        "abdominal pain, and sometimes fever."
    ),
    "Acute coronary syndrome": (
        "Acute coronary syndrome must be considered when chest pain occurs "
        "with dyspnea, sweating, or nausea. Urgent clinical assessment is required."
    ),
    "Asthma exacerbation": (
        "Asthma exacerbation is considered when wheeze, dyspnea, cough, "
        "and chest tightness occur together."
    ),
}


INVESTIGATIONS = {
    "Pneumonia": [
        "Chest radiograph",
        "Pulse oximetry",
        "Complete blood count when clinically indicated",
    ],
    "Upper respiratory infection": [
        "Focused clinical examination",
        "Additional investigations only if clinically indicated",
    ],
    "Urinary tract infection": [
        "Urinalysis",
        "Urine culture when clinically indicated",
    ],
    "Gastroenteritis": [
        "Hydration assessment",
        "Serum electrolytes when dehydration is suspected",
    ],
    "Acute coronary syndrome": [
        "12-lead ECG",
        "Cardiac biomarkers",
        "Urgent clinical assessment",
    ],
    "Asthma exacerbation": [
        "Pulse oximetry",
        "Peak expiratory flow when appropriate",
        "Focused respiratory assessment",
    ],
}


def reason_from_symptoms(symptoms):
    """
    Rank differential diagnoses using transparent weighted rules.

    This educational engine demonstrates symptom-to-diagnosis reasoning.
    """

    active = {
        key
        for key, value in symptoms.items()
        if bool(value)
    }

    ranked = []

    for disease, rules in DISEASE_RULES.items():
        score = 0
        matched = []

        for symptom, weight in rules.items():
            if symptom in active:
                score += weight
                matched.append({
                    "symptom": symptom,
                    "weight": weight,
                })

        maximum = sum(rules.values())

        normalized_score = (
            score / maximum
            if maximum
            else 0
        )

        if score > 0:
            ranked.append({
                "diagnosis": disease,
                "score": score,
                "normalized_score": normalized_score,
                "matched_features": matched,
                "explanation": EXPLANATIONS[disease],
                "investigations": INVESTIGATIONS[disease],
            })

    ranked.sort(
        key=lambda item: (
            item["normalized_score"],
            item["score"],
        ),
        reverse=True,
    )

    if not ranked:
        return {
            "differentials": [],
            "leading_diagnosis": None,
            "logic": (
                "No predefined disease rule matched the selected symptoms."
            ),
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION,
            "disclaimer": (
                "Educational clinical reasoning prototype only. "
                "It does not establish a diagnosis."
            ),
        }

    leading = ranked[0]

    matched_terms = [
        item["symptom"].replace("_", " ")
        for item in leading["matched_features"]
    ]

    logic = (
        f"{leading['diagnosis']} ranked highest because the case matched: "
        + ", ".join(matched_terms)
        + "."
    )

    return {
        "differentials": ranked,
        "leading_diagnosis": leading["diagnosis"],
        "logic": logic,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "disclaimer": (
            "Educational clinical reasoning prototype only. "
            "Differential diagnoses require clinician assessment and "
            "must not be treated as autonomous diagnostic conclusions."
        ),
    }
