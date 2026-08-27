MODEL_NAME = "iHIS Oncology DFS Reasoning Engine"
MODEL_VERSION = "1.0"


TREE = {
    "Cancer-related presentation": [
        "Thoracic pathway",
        "Gastrointestinal pathway",
        "Genitourinary pathway",
    ],

    "Thoracic pathway": [
        "Lung cancer pathway",
    ],

    "Gastrointestinal pathway": [
        "Colorectal cancer pathway",
    ],

    "Genitourinary pathway": [
        "Prostate cancer pathway",
    ],
}


CATEGORY_GATES = {
    "Thoracic pathway": {
        "persistent_cough",
        "hemoptysis",
        "dyspnea",
        "chest_pain",
        "weight_loss",
    },

    "Gastrointestinal pathway": {
        "rectal_bleeding",
        "change_bowel_habit",
        "abdominal_pain",
        "weight_loss",
    },

    "Genitourinary pathway": {
        "urinary_obstruction",
        "hematuria",
        "bone_pain",
        "weight_loss",
    },
}


PATHWAY_RULES = {
    "Lung cancer pathway": {
        "features": {
            "persistent_cough": 3,
            "hemoptysis": 5,
            "dyspnea": 2,
            "chest_pain": 2,
            "weight_loss": 3,
            "smoking_history": 3,
        },

        "investigations": [
            "Chest imaging",
            "Contrast-enhanced CT of the chest when appropriate",
            "Tissue diagnosis when clinically indicated",
        ],

        "staging": [
            "Assess regional lymph nodes",
            "Evaluate for distant metastatic disease",
            "Assign TNM stage after adequate diagnostic work-up",
        ],
    },

    "Colorectal cancer pathway": {
        "features": {
            "rectal_bleeding": 5,
            "change_bowel_habit": 4,
            "abdominal_pain": 2,
            "weight_loss": 3,
            "anemia": 3,
        },

        "investigations": [
            "Lower gastrointestinal endoscopic assessment",
            "Histopathologic confirmation when a lesion is identified",
            "Cross-sectional imaging for staging when appropriate",
        ],

        "staging": [
            "Assess primary tumor extent",
            "Assess regional lymph nodes",
            "Evaluate for distant metastatic disease",
        ],
    },

    "Prostate cancer pathway": {
        "features": {
            "urinary_obstruction": 3,
            "hematuria": 2,
            "bone_pain": 4,
            "weight_loss": 2,
            "elevated_psa": 5,
        },

        "investigations": [
            "Clinical assessment including prostate evaluation",
            "PSA assessment when clinically appropriate",
            "Prostate imaging and tissue diagnosis when indicated",
        ],

        "staging": [
            "Assess local disease extent",
            "Assess nodal involvement",
            "Evaluate for metastatic disease, particularly bone involvement",
        ],
    },
}


def dfs_oncology_reasoning(symptoms):
    """
    Explore cancer-related diagnostic pathways using true Depth-First Search.
    """

    active = {
        key
        for key, value in symptoms.items()
        if bool(value)
    }

    stack = ["Cancer-related presentation"]

    visited = []
    candidates = []

    while stack:
        node = stack.pop()
        visited.append(node)

        if node == "Cancer-related presentation":
            # Reverse so Thoracic is explored first by the stack.
            for child in reversed(TREE[node]):
                stack.append(child)
            continue

        if node in CATEGORY_GATES:
            if active.intersection(
                CATEGORY_GATES[node]
            ):
                for child in reversed(
                    TREE[node]
                ):
                    stack.append(child)
            continue

        rule = PATHWAY_RULES.get(node)

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

        normalized_score = (
            score / maximum
            if maximum
            else 0
        )

        if score > 0:
            candidates.append({
                "pathway": node,
                "score": score,
                "normalized_score": normalized_score,
                "matched_features": matched,
                "investigations": rule["investigations"],
                "staging": rule["staging"],
            })

    candidates.sort(
        key=lambda item: (
            item["normalized_score"],
            item["score"],
        ),
        reverse=True,
    )

    leading = (
        candidates[0]
        if candidates
        else None
    )

    return {
        "leading_pathway": (
            leading["pathway"]
            if leading
            else None
        ),

        "candidates": candidates,

        "dfs_visit_order": visited,

        "investigations": (
            leading["investigations"]
            if leading
            else []
        ),

        "staging": (
            leading["staging"]
            if leading
            else []
        ),

        "algorithm": "Depth-First Search (DFS)",

        "model_name": MODEL_NAME,

        "model_version": MODEL_VERSION,

        "disclaimer": (
            "Educational oncology reasoning prototype only. "
            "These pathways do not establish a cancer diagnosis, "
            "stage, or treatment recommendation."
        ),
    }
