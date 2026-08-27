from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    ROOT
    / "model_artifacts"
    / "gp_disease_model.joblib"
)


FEATURES = [
    "age",
    "temperature",
    "heart_rate",
    "cough",
    "sputum",
    "dyspnea",
    "dysuria",
    "urinary_frequency",
    "abdominal_pain",
    "diarrhea",
    "vomiting",
    "smoking",
]


INVESTIGATION_MAP = {
    "Upper respiratory infection": [
        "Focused clinical examination",
        "Consider CBC if symptoms are persistent or clinically indicated",
    ],
    "Pneumonia": [
        "Chest radiograph",
        "Complete blood count",
        "Pulse oximetry",
    ],
    "Urinary tract infection": [
        "Urinalysis",
        "Urine culture when clinically indicated",
    ],
    "Gastroenteritis": [
        "Clinical hydration assessment",
        "Serum electrolytes if dehydration or significant illness is suspected",
        "CBC when clinically indicated",
    ],
}


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "GP model artifact not found. "
            "Run scripts/train_gp_model.py first."
        )

    return joblib.load(MODEL_PATH)


def identify_risk_factors(data):
    factors = []

    if data["age"] >= 65:
        factors.append("Age 65 years or older")

    if data["temperature"] >= 38.5:
        factors.append("High fever")

    if data["heart_rate"] >= 100:
        factors.append("Tachycardia")

    if data["dyspnea"]:
        factors.append("Reported dyspnea")

    if data["smoking"]:
        factors.append("Smoking")

    if not factors:
        factors.append(
            "No predefined high-risk feature detected by this simple module"
        )

    return factors


def predict_gp_case(data):
    model = load_model()

    row = pd.DataFrame(
        [
            {
                "age": int(data["age"]),
                "temperature": float(data["temperature"]),
                "heart_rate": int(data["heart_rate"]),
                "cough": int(bool(data["cough"])),
                "sputum": int(bool(data["sputum"])),
                "dyspnea": int(bool(data["dyspnea"])),
                "dysuria": int(bool(data["dysuria"])),
                "urinary_frequency": int(
                    bool(data["urinary_frequency"])
                ),
                "abdominal_pain": int(
                    bool(data["abdominal_pain"])
                ),
                "diarrhea": int(bool(data["diarrhea"])),
                "vomiting": int(bool(data["vomiting"])),
                "smoking": int(bool(data["smoking"])),
            }
        ],
        columns=FEATURES,
    )

    probabilities = model.predict_proba(row)[0]
    classes = model.named_steps["model"].classes_

    ranked = sorted(
        zip(classes, probabilities),
        key=lambda item: item[1],
        reverse=True,
    )

    predicted_condition = ranked[0][0]

    return {
        "predicted_condition": predicted_condition,
        "confidence": float(ranked[0][1]),
        "ranked_predictions": [
            {
                "condition": condition,
                "probability": float(probability),
            }
            for condition, probability in ranked
        ],
        "risk_factors": identify_risk_factors(data),
        "recommended_investigations": INVESTIGATION_MAP[
            predicted_condition
        ],
        "model_name": "iHIS GP Multiclass Logistic Regression",
        "model_version": "1.0",
        "disclaimer": (
            "Educational AI prediction only. "
            "The model was trained on synthetic data and is not "
            "clinically validated for diagnosis or treatment."
        ),
    }
