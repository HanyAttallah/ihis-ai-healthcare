MODEL_NAME = "iHIS Radiation Oncology CTCAE Toxicity Support Engine"
MODEL_VERSION = "2.0 — CTCAE v5.0"


CTCAE_LABELS = {
    "mucositis_oral": {
        0: "No oral mucositis",
        1: "Grade 1 — Asymptomatic or mild symptoms; intervention not indicated",
        2: "Grade 2 — Moderate pain or ulcer not interfering with oral intake; modified diet indicated",
        3: "Grade 3 — Severe pain; interfering with oral intake",
        4: "Grade 4 — Life-threatening consequences; urgent intervention indicated",
    },

    "dermatitis_radiation": {
        0: "No radiation dermatitis",
        1: "Grade 1 — Faint erythema or dry desquamation",
        2: "Grade 2 — Moderate/brisk erythema; patchy moist desquamation mainly in folds/creases; moderate edema",
        3: "Grade 3 — Moist desquamation outside skin folds/creases; bleeding induced by minor trauma or abrasion",
        4: "Grade 4 — Life-threatening consequences; full-thickness skin necrosis/ulceration or spontaneous bleeding; skin graft indicated",
    },

    "dysphagia": {
        0: "No dysphagia",
        1: "Grade 1 — Symptomatic, able to eat regular diet",
        2: "Grade 2 — Symptomatic with altered eating/swallowing",
        3: "Grade 3 — Severely altered eating/swallowing; tube feeding, TPN, or hospitalization indicated",
        4: "Grade 4 — Life-threatening consequences; urgent intervention indicated",
    },

    "nausea": {
        0: "No nausea",
        1: "Grade 1 — Loss of appetite without alteration in eating habits",
        2: "Grade 2 — Oral intake decreased without significant weight loss, dehydration, or malnutrition",
        3: "Grade 3 — Inadequate oral caloric/fluid intake; tube feeding, TPN, or hospitalization indicated",
    },

    "vomiting": {
        0: "No vomiting",
        1: "Grade 1 — Intervention not indicated",
        2: "Grade 2 — Outpatient IV hydration; medical intervention indicated",
        3: "Grade 3 — Tube feeding, TPN, or hospitalization indicated",
        4: "Grade 4 — Life-threatening consequences",
    },

    "fatigue": {
        0: "No fatigue",
        1: "Grade 1 — Fatigue relieved by rest",
        2: "Grade 2 — Fatigue not relieved by rest; limiting instrumental ADL",
        3: "Grade 3 — Fatigue not relieved by rest; limiting self-care ADL",
    },
}


DISPLAY_NAMES = {
    "mucositis_oral": "Oral mucositis",
    "dermatitis_radiation": "Radiation dermatitis",
    "dysphagia": "Dysphagia",
    "nausea": "Nausea",
    "vomiting": "Vomiting",
    "fatigue": "Fatigue",
}


def pain_category(score):
    """
    Application-level descriptive grouping for the 0–10 pain scale.
    This grouping is not presented as a CTCAE grade.
    """

    score = int(score)

    if score == 0:
        return "No pain"

    if score <= 3:
        return "Low-intensity pain"

    if score <= 6:
        return "Moderate-intensity pain"

    return "High-intensity pain"


def analyze_rt_toxicity(
    mucositis_oral,
    dermatitis_radiation,
    dysphagia,
    nausea,
    vomiting,
    fatigue,
    pain_score,
    weight_loss,
    fever,
):
    grades = {
        "mucositis_oral": int(mucositis_oral),
        "dermatitis_radiation": int(dermatitis_radiation),
        "dysphagia": int(dysphagia),
        "nausea": int(nausea),
        "vomiting": int(vomiting),
        "fatigue": int(fatigue),
    }

    pain_score = int(pain_score)

    toxicity_summary = []

    for key, grade in grades.items():
        toxicity_summary.append({
            "key": key,
            "name": DISPLAY_NAMES[key],
            "grade": grade,
            "description": CTCAE_LABELS[key][grade],
        })

    grade_4 = [
        DISPLAY_NAMES[key]
        for key, grade in grades.items()
        if grade >= 4
    ]

    grade_3 = [
        DISPLAY_NAMES[key]
        for key, grade in grades.items()
        if grade == 3
    ]

    grade_2 = [
        DISPLAY_NAMES[key]
        for key, grade in grades.items()
        if grade == 2
    ]

    alerts = []

    if weight_loss:
        alerts.append(
            "Clinically relevant weight loss reported."
        )

    if fever:
        alerts.append(
            "Fever reported during radiotherapy."
        )

    if pain_score >= 7:
        alerts.append(
            f"High pain score reported: {pain_score}/10."
        )

    if grade_4:
        review_level = "Immediate / Urgent Radiation Oncology Review"

        recommendation = (
            "One or more CTCAE Grade 4 toxicities are recorded. "
            "Immediate clinical assessment and appropriate urgent "
            "management are required."
        )

    elif grade_3 or fever:
        review_level = "Urgent Radiation Oncology Review"

        recommendation = (
            "CTCAE Grade 3 toxicity or another significant clinical "
            "alert is present. Prompt radiation-oncology assessment "
            "is recommended before proceeding with the treatment pathway."
        )

    elif grade_2 or weight_loss or pain_score >= 7:
        review_level = "Early On-Treatment Review"

        recommendation = (
            "Moderate treatment-related toxicity or another clinically "
            "important symptom is present. Arrange early review and "
            "optimize supportive care."
        )

    else:
        review_level = "Routine On-Treatment Review"

        recommendation = (
            "No CTCAE Grade 2–4 toxicity or predefined major alert "
            "was detected. Continue routine on-treatment assessment "
            "and reassess if symptoms change."
        )

    return {
        "toxicity_summary": toxicity_summary,
        "grade_4_toxicities": grade_4,
        "grade_3_toxicities": grade_3,
        "grade_2_toxicities": grade_2,
        "pain_score": pain_score,
        "pain_category": pain_category(pain_score),
        "alerts": alerts,
        "review_level": review_level,
        "recommendation": recommendation,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "department": "Radiation Oncology",
        "reference_standard": "NCI CTCAE v5.0",
        "disclaimer": (
            "Educational Radiation Oncology decision-support prototype. "
            "CTCAE terminology is used for structured toxicity recording, "
            "but clinical grading and treatment decisions require clinician "
            "assessment. The 0–10 pain score is recorded separately and is "
            "not itself a CTCAE grade."
        ),
    }
