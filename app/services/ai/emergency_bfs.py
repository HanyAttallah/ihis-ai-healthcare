from collections import deque


MODEL_NAME = "iHIS Emergency BFS Decision-Support Engine"
MODEL_VERSION = "1.0"


TREE = {
    "Emergency Presentation": [
        "Cardiorespiratory",
        "Neurological",
        "Systemic / Infectious",
    ],
    "Cardiorespiratory": [
        "Acute coronary syndrome",
        "Pulmonary embolism",
        "Asthma exacerbation",
    ],
    "Neurological": [
        "Stroke",
        "Seizure",
    ],
    "Systemic / Infectious": [
        "Sepsis",
        "Anaphylaxis",
    ],
}


CATEGORY_GATES = {
    "Cardiorespiratory": {
        "chest_pain",
        "dyspnea",
        "wheeze",
        "tachycardia",
        "hemoptysis",
    },
    "Neurological": {
        "sudden_weakness",
        "speech_difficulty",
        "seizure",
    },
    "Systemic / Infectious": {
        "fever",
        "hypotension",
        "rash",
        "swelling",
        "tachycardia",
    },
}


CONDITION_RULES = {
    "Acute coronary syndrome": {
        "priority": "Emergency",
        "features": {
            "chest_pain": 5,
            "dyspnea": 2,
            "sweating": 2,
            "nausea": 1,
        },
        "action": (
            "Urgent clinician assessment, ECG, and cardiac biomarker "
            "evaluation according to local emergency protocol."
        ),
    },
    "Pulmonary embolism": {
        "priority": "Emergency",
        "features": {
            "dyspnea": 4,
            "chest_pain": 3,
            "tachycardia": 2,
            "hemoptysis": 3,
        },
        "action": (
            "Urgent clinical probability assessment and appropriate "
            "investigation according to local protocol."
        ),
    },
    "Asthma exacerbation": {
        "priority": "Urgent",
        "features": {
            "dyspnea": 4,
            "wheeze": 5,
            "chest_tightness": 3,
        },
        "action": (
            "Assess respiratory status, oxygenation, and need for "
            "urgent bronchodilator therapy according to local protocol."
        ),
    },
    "Stroke": {
        "priority": "Emergency",
        "features": {
            "sudden_weakness": 5,
            "speech_difficulty": 5,
        },
        "action": (
            "Activate urgent stroke assessment and time-critical "
            "neuroimaging pathway."
        ),
    },
    "Seizure": {
        "priority": "Emergency",
        "features": {
            "seizure": 6,
            "altered_consciousness": 3,
        },
        "action": (
            "Immediate airway and safety assessment with urgent "
            "clinical evaluation."
        ),
    },
    "Sepsis": {
        "priority": "Emergency",
        "features": {
            "fever": 3,
            "hypotension": 5,
            "tachycardia": 2,
            "altered_consciousness": 3,
        },
        "action": (
            "Urgent sepsis assessment and resuscitation pathway "
            "according to local protocol."
        ),
    },
    "Anaphylaxis": {
        "priority": "Emergency",
        "features": {
            "swelling": 5,
            "rash": 2,
            "dyspnea": 5,
            "hypotension": 4,
        },
        "action": (
            "Immediate emergency assessment for possible anaphylaxis "
            "and treatment according to local protocol."
        ),
    },
}


def bfs_emergency_reasoning(symptoms):
    """
    Explore an emergency diagnostic tree using true Breadth-First Search.
    """

    active = {
        key
        for key, value in symptoms.items()
        if bool(value)
    }

    queue = deque(
        ["Emergency Presentation"]
    )

    visited = []
    candidates = []

    while queue:
        node = queue.popleft()
        visited.append(node)

        if node == "Emergency Presentation":
            for child in TREE[node]:
                queue.append(child)

            continue

        if node in CATEGORY_GATES:
            gate_features = CATEGORY_GATES[node]

            if active.intersection(gate_features):
                for child in TREE[node]:
                    queue.append(child)

            continue

        rule = CONDITION_RULES.get(node)

        if not rule:
            continue

        score = 0
        matched = []

        for feature, weight in rule["features"].items():
            if feature in active:
                score += weight
                matched.append({
                    "feature": feature,
                    "weight": weight,
                })

        maximum = sum(
            rule["features"].values()
        )

        normalized = (
            score / maximum
            if maximum
            else 0
        )

        if score > 0:
            candidates.append({
                "condition": node,
                "priority": rule["priority"],
                "score": score,
                "normalized_score": normalized,
                "matched_features": matched,
                "recommended_action": rule["action"],
            })

    candidates.sort(
        key=lambda item: (
            1 if item["priority"] == "Emergency" else 0,
            item["normalized_score"],
            item["score"],
        ),
        reverse=True,
    )

    emergency_candidates = [
        item
        for item in candidates
        if (
            item["priority"] == "Emergency"
            and item["normalized_score"] >= 0.35
        )
    ]

    if emergency_candidates:
        triage = "Emergency"
        overall_action = (
            "Immediate emergency clinician assessment is required. "
            "Use airway, breathing, circulation and local emergency "
            "escalation protocols."
        )

    elif candidates:
        triage = "Urgent"
        overall_action = (
            "Prompt clinician assessment is recommended because "
            "one or more emergency diagnostic pathways were matched."
        )

    else:
        triage = "No predefined emergency pathway matched"
        overall_action = (
            "No predefined BFS emergency pathway matched the selected "
            "features. Clinical assessment remains necessary."
        )

    leading = (
        candidates[0]["condition"]
        if candidates
        else None
    )

    return {
        "triage": triage,
        "leading_possibility": leading,
        "candidates": candidates,
        "bfs_visit_order": visited,
        "overall_action": overall_action,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "algorithm": "Breadth-First Search (BFS)",
        "disclaimer": (
            "Educational emergency decision-support prototype only. "
            "It does not establish a diagnosis and must not delay "
            "emergency assessment or local escalation procedures."
        ),
    }
