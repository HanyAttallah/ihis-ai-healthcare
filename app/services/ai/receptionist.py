import re


MODEL_NAME = "iHIS Receptionist Routing Expert System"
MODEL_VERSION = "1.0"


RED_FLAG_RULES = {
    "severe breathing difficulty": [
        "severe shortness of breath",
        "severe difficulty breathing",
        "cannot breathe",
        "struggling to breathe",
    ],
    "possible acute coronary syndrome": [
        "crushing chest pain",
        "severe chest pain",
        "chest pressure",
    ],
    "loss of consciousness": [
        "unconscious",
        "loss of consciousness",
        "passed out",
        "fainted and not waking",
    ],
    "possible acute neurological emergency": [
        "face drooping",
        "facial droop",
        "slurred speech",
        "sudden weakness",
        "one sided weakness",
        "one-sided weakness",
    ],
    "active seizure": [
        "active seizure",
        "currently seizing",
        "convulsing",
    ],
    "severe bleeding": [
        "severe bleeding",
        "heavy bleeding",
        "uncontrolled bleeding",
    ],
    "possible anaphylaxis": [
        "swollen tongue",
        "throat swelling",
        "anaphylaxis",
    ],
}


ROUTING_RULES = {
    "Emergency Department": {
        "weight": 10,
        "terms": [],
    },
    "General Medicine": {
        "weight": 3,
        "terms": [
            "fever",
            "fatigue",
            "cough",
            "weakness",
            "dizziness",
            "headache",
            "vomiting",
            "nausea",
        ],
    },
    "Respiratory Medicine": {
        "weight": 5,
        "terms": [
            "cough",
            "productive cough",
            "shortness of breath",
            "wheezing",
            "breathlessness",
            "sputum",
        ],
    },
    "Cardiology": {
        "weight": 5,
        "terms": [
            "palpitation",
            "palpitations",
            "chest discomfort",
            "exertional chest pain",
            "irregular heartbeat",
        ],
    },
    "Neurology": {
        "weight": 5,
        "terms": [
            "seizure",
            "numbness",
            "tingling",
            "migraine",
            "tremor",
            "memory problem",
        ],
    },
    "Gastroenterology": {
        "weight": 5,
        "terms": [
            "abdominal pain",
            "diarrhea",
            "constipation",
            "blood in stool",
            "indigestion",
            "difficulty swallowing",
        ],
    },
    "Orthopedics": {
        "weight": 5,
        "terms": [
            "joint pain",
            "back pain",
            "knee pain",
            "shoulder pain",
            "bone pain",
            "sprain",
        ],
    },
    "Dermatology": {
        "weight": 5,
        "terms": [
            "rash",
            "skin lesion",
            "itching",
            "skin swelling",
        ],
    },
}


NEGATION_PATTERNS = [
    r"\bno\s+{term}\b",
    r"\bdenies\s+{term}\b",
    r"\bwithout\s+{term}\b",
]


def _normalize_text(text):
    """Normalize free-text intake for deterministic rule matching."""

    text = (text or "").lower()

    text = re.sub(
        r"[^a-z0-9\s\-]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def _term_is_negated(text, term):
    """Detect simple explicit negation immediately preceding a term."""

    escaped_term = re.escape(term)

    for pattern in NEGATION_PATTERNS:
        expression = pattern.format(
            term=escaped_term
        )

        if re.search(expression, text):
            return True

    return False


def _term_present(text, term):
    """Return True when a non-negated routing term is present."""

    if term not in text:
        return False

    return not _term_is_negated(
        text,
        term,
    )


def detect_red_flags(text):
    """Return explainable red flags detected in intake text."""

    detected = []

    for label, phrases in RED_FLAG_RULES.items():
        matched_phrases = []

        for phrase in phrases:
            if _term_present(text, phrase):
                matched_phrases.append(
                    phrase
                )

        if matched_phrases:
            detected.append(
                {
                    "red_flag": label,
                    "matched_terms": matched_phrases,
                }
            )

    return detected


def score_departments(text):
    """Calculate transparent department-routing scores."""

    scores = {}
    evidence = {}

    for department, rule in ROUTING_RULES.items():
        if department == "Emergency Department":
            continue

        matched = []

        for term in rule["terms"]:
            if _term_present(text, term):
                matched.append(term)

        if matched:
            scores[department] = (
                len(matched) * rule["weight"]
            )

            evidence[department] = matched

    return scores, evidence


def determine_urgency(red_flags, symptom_duration=None):
    """Assign a non-diagnostic receptionist urgency category."""

    if red_flags:
        return "Emergency"

    duration = (
        symptom_duration or ""
    ).strip().lower()

    urgent_terms = [
        "today",
        "hours",
        "hour",
        "1 day",
        "one day",
        "2 days",
        "two days",
        "3 days",
        "three days",
    ]

    if any(
        term in duration
        for term in urgent_terms
    ):
        return "Prompt"

    return "Routine"


def generate_basic_guidance(
    recommended_service,
    urgency,
    red_flags,
):
    """Generate simple non-diagnostic routing and appointment guidance."""

    if urgency == "Emergency":
        return (
            "Proceed immediately for emergency assessment. "
            "Do not wait for a routine outpatient appointment.",
            "Immediate Emergency Department assessment",
        )

    if urgency == "Prompt":
        return (
            f"Arrange prompt assessment by {recommended_service}. "
            "Seek emergency assessment if symptoms become severe "
            "or new red-flag symptoms develop.",
            "Same-day or earliest available appointment",
        )

    return (
        f"Arrange routine assessment by {recommended_service}. "
        "Seek earlier medical assessment if symptoms worsen.",
        "Next available outpatient appointment",
    )

def route_patient(
    symptom_text,
    symptom_duration=None,
):
    """
    Generate a non-diagnostic receptionist routing recommendation.

    This is a symbolic expert system. It does not provide a diagnosis
    and requires human review before operational use.
    """

    normalized_text = _normalize_text(
        symptom_text
    )

    red_flags = detect_red_flags(
        normalized_text
    )

    urgency = determine_urgency(
        red_flags,
        symptom_duration,
    )

    scores, evidence = score_departments(
        normalized_text
    )

    if red_flags:
        recommended_service = (
            "Emergency Department"
        )

        explanation = (
            "Emergency routing was triggered because "
            "one or more predefined red-flag patterns "
            "were detected. Immediate human assessment "
            "is required."
        )

    elif scores:
        recommended_service = max(
            scores,
            key=scores.get,
        )

        matched = evidence.get(
            recommended_service,
            [],
        )

        explanation = (
            "The recommended service was selected by "
            "matching the reported symptoms against "
            "transparent routing rules. Matched terms "
            f"for {recommended_service}: "
            f"{', '.join(matched)}."
        )

    else:
        recommended_service = (
            "General Medicine"
        )

        explanation = (
            "No specialty-specific routing rule reached "
            "a match. General Medicine is suggested as "
            "the default entry point for human clinical "
            "assessment."
        )

    basic_guidance, appointment_information = generate_basic_guidance(
        recommended_service,
        urgency,
        red_flags,
    )

    return {
        "recommended_service": recommended_service,
        "urgency": urgency,
        "red_flags": red_flags,
        "department_scores": scores,
        "routing_evidence": evidence,
        "explanation": explanation,
        "basic_guidance": basic_guidance,
        "appointment_information": appointment_information,
        "disclaimer": (
            "This output is administrative clinical "
            "decision support only. It is not a diagnosis "
            "and requires human review."
        ),
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
    }


