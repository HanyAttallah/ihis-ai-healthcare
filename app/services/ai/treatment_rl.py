import random


MODEL_NAME = "iHIS Treatment Planning Q-Learning Simulation"
MODEL_VERSION = "1.1 — ECOG"


ACTIONS = [
    "Local therapy",
    "Systemic therapy",
    "Combined modality therapy",
    "Supportive / symptom-directed care",
]


ECOG_DESCRIPTIONS = {
    "0": "Fully active",
    "1": "Restricted in strenuous activity but ambulatory",
    "2": "Ambulatory and capable of self-care but unable to work",
    "3": "Limited self-care; confined to bed or chair for more than 50% of waking hours",
    "4": "Completely disabled; unable to carry out self-care",
}


# Synthetic educational reward environment.
# These values are NOT clinical treatment guidelines.
REWARD_TABLE = {
    ("Localized", "0"): {
        "Local therapy": 9,
        "Systemic therapy": 3,
        "Combined modality therapy": 6,
        "Supportive / symptom-directed care": 1,
    },
    ("Localized", "1"): {
        "Local therapy": 8,
        "Systemic therapy": 4,
        "Combined modality therapy": 6,
        "Supportive / symptom-directed care": 2,
    },
    ("Localized", "2"): {
        "Local therapy": 6,
        "Systemic therapy": 4,
        "Combined modality therapy": 4,
        "Supportive / symptom-directed care": 4,
    },
    ("Localized", "3"): {
        "Local therapy": 3,
        "Systemic therapy": 2,
        "Combined modality therapy": 1,
        "Supportive / symptom-directed care": 7,
    },
    ("Localized", "4"): {
        "Local therapy": 1,
        "Systemic therapy": 1,
        "Combined modality therapy": 0,
        "Supportive / symptom-directed care": 9,
    },

    ("Locally advanced", "0"): {
        "Local therapy": 4,
        "Systemic therapy": 6,
        "Combined modality therapy": 9,
        "Supportive / symptom-directed care": 1,
    },
    ("Locally advanced", "1"): {
        "Local therapy": 4,
        "Systemic therapy": 6,
        "Combined modality therapy": 8,
        "Supportive / symptom-directed care": 2,
    },
    ("Locally advanced", "2"): {
        "Local therapy": 3,
        "Systemic therapy": 5,
        "Combined modality therapy": 6,
        "Supportive / symptom-directed care": 4,
    },
    ("Locally advanced", "3"): {
        "Local therapy": 2,
        "Systemic therapy": 3,
        "Combined modality therapy": 2,
        "Supportive / symptom-directed care": 7,
    },
    ("Locally advanced", "4"): {
        "Local therapy": 1,
        "Systemic therapy": 1,
        "Combined modality therapy": 0,
        "Supportive / symptom-directed care": 9,
    },

    ("Metastatic", "0"): {
        "Local therapy": 2,
        "Systemic therapy": 9,
        "Combined modality therapy": 4,
        "Supportive / symptom-directed care": 2,
    },
    ("Metastatic", "1"): {
        "Local therapy": 2,
        "Systemic therapy": 8,
        "Combined modality therapy": 4,
        "Supportive / symptom-directed care": 3,
    },
    ("Metastatic", "2"): {
        "Local therapy": 1,
        "Systemic therapy": 6,
        "Combined modality therapy": 3,
        "Supportive / symptom-directed care": 5,
    },
    ("Metastatic", "3"): {
        "Local therapy": 1,
        "Systemic therapy": 3,
        "Combined modality therapy": 1,
        "Supportive / symptom-directed care": 8,
    },
    ("Metastatic", "4"): {
        "Local therapy": 0,
        "Systemic therapy": 1,
        "Combined modality therapy": 0,
        "Supportive / symptom-directed care": 9,
    },
}


def train_q_learning(
    episodes=8000,
    alpha=0.20,
    epsilon=0.20,
    seed=42,
):
    """
    Train a simple one-step educational Q-learning simulation.
    """

    rng = random.Random(seed)

    states = list(REWARD_TABLE.keys())

    q_table = {
        state: {
            action: 0.0
            for action in ACTIONS
        }
        for state in states
    }

    for _ in range(episodes):
        state = rng.choice(states)

        if rng.random() < epsilon:
            action = rng.choice(ACTIONS)
        else:
            action = max(
                q_table[state],
                key=q_table[state].get,
            )

        reward = REWARD_TABLE[state][action]

        q_table[state][action] += (
            alpha
            * (
                reward
                - q_table[state][action]
            )
        )

    return q_table


Q_TABLE = train_q_learning()


def optimize_treatment(
    disease_extent,
    ecog_status,
):
    state = (
        disease_extent,
        str(ecog_status),
    )

    if state not in Q_TABLE:
        raise ValueError(
            "Unsupported disease extent or ECOG status."
        )

    values = Q_TABLE[state]

    ranked = sorted(
        values.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    recommended = ranked[0][0]

    return {
        "state": {
            "disease_extent": disease_extent,
            "ecog_status": str(ecog_status),
            "ecog_description": ECOG_DESCRIPTIONS[
                str(ecog_status)
            ],
        },

        "recommended_strategy": recommended,

        "alternatives": [
            {
                "strategy": action,
                "learned_value": round(
                    value,
                    3,
                ),
            }
            for action, value in ranked
        ],

        "evaluation": (
            "The Q-learning simulation compared alternative management "
            "strategies using disease extent and ECOG Performance Status. "
            f"For the simulated state {disease_extent}, ECOG "
            f"{ecog_status}, the highest learned utility was "
            f"{recommended}."
        ),

        "algorithm": "Q-learning",

        "model_name": MODEL_NAME,

        "model_version": MODEL_VERSION,

        "disclaimer": (
            "Educational reinforcement-learning simulation only. "
            "The reward values are synthetic and do not represent "
            "oncology guidelines, clinical trial evidence, validated "
            "treatment recommendations, or individual patient care."
        ),
    }
