from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "model_artifacts"
RESULTS_DIR = ROOT / "docs" / "deliverables" / "week_02" / "results"

DATA_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


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


rng = np.random.default_rng(42)


def yes(probability):
    return int(rng.random() < probability)


def noisy(value, probability=0.06):
    if rng.random() < probability:
        return 1 - value
    return value


def make_case(label):
    if label == "Upper respiratory infection":
        row = {
            "age": int(np.clip(rng.normal(38, 17), 18, 85)),
            "temperature": float(np.clip(rng.normal(37.7, 0.45), 35.5, 41.5)),
            "heart_rate": int(np.clip(rng.normal(84, 11), 50, 160)),
            "cough": yes(0.88),
            "sputum": yes(0.25),
            "dyspnea": yes(0.08),
            "dysuria": yes(0.03),
            "urinary_frequency": yes(0.04),
            "abdominal_pain": yes(0.06),
            "diarrhea": yes(0.04),
            "vomiting": yes(0.03),
            "smoking": yes(0.22),
        }

    elif label == "Pneumonia":
        row = {
            "age": int(np.clip(rng.normal(55, 18), 18, 90)),
            "temperature": float(np.clip(rng.normal(38.7, 0.55), 35.5, 41.5)),
            "heart_rate": int(np.clip(rng.normal(106, 14), 50, 170)),
            "cough": yes(0.94),
            "sputum": yes(0.78),
            "dyspnea": yes(0.64),
            "dysuria": yes(0.02),
            "urinary_frequency": yes(0.03),
            "abdominal_pain": yes(0.05),
            "diarrhea": yes(0.04),
            "vomiting": yes(0.05),
            "smoking": yes(0.32),
        }

    elif label == "Urinary tract infection":
        row = {
            "age": int(np.clip(rng.normal(46, 19), 18, 90)),
            "temperature": float(np.clip(rng.normal(37.8, 0.65), 35.5, 41.5)),
            "heart_rate": int(np.clip(rng.normal(88, 13), 50, 160)),
            "cough": yes(0.04),
            "sputum": yes(0.02),
            "dyspnea": yes(0.03),
            "dysuria": yes(0.90),
            "urinary_frequency": yes(0.84),
            "abdominal_pain": yes(0.34),
            "diarrhea": yes(0.04),
            "vomiting": yes(0.09),
            "smoking": yes(0.20),
        }

    else:
        row = {
            "age": int(np.clip(rng.normal(35, 16), 18, 85)),
            "temperature": float(np.clip(rng.normal(37.8, 0.50), 35.5, 41.5)),
            "heart_rate": int(np.clip(rng.normal(91, 13), 50, 160)),
            "cough": yes(0.03),
            "sputum": yes(0.01),
            "dyspnea": yes(0.02),
            "dysuria": yes(0.02),
            "urinary_frequency": yes(0.03),
            "abdominal_pain": yes(0.76),
            "diarrhea": yes(0.91),
            "vomiting": yes(0.69),
            "smoking": yes(0.18),
        }

    for feature in [
        "cough",
        "sputum",
        "dyspnea",
        "dysuria",
        "urinary_frequency",
        "abdominal_pain",
        "diarrhea",
        "vomiting",
    ]:
        row[feature] = noisy(row[feature])

    row["diagnosis"] = label
    return row


labels = [
    "Upper respiratory infection",
    "Pneumonia",
    "Urinary tract infection",
    "Gastroenteritis",
]

rows = []

for label in labels:
    for _ in range(400):
        rows.append(make_case(label))

df = pd.DataFrame(rows)

dataset_path = DATA_DIR / "gp_week2_synthetic.csv"
df.to_csv(dataset_path, index=False)

X = df[FEATURES]
y = df["diagnosis"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

model = Pipeline(
    [
        ("scale", StandardScaler()),
        (
            "model",
            LogisticRegression(
                max_iter=2000,
                random_state=42,
            ),
        ),
    ]
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
macro_f1 = f1_score(
    y_test,
    predictions,
    average="macro",
)

report = classification_report(
    y_test,
    predictions,
    output_dict=True,
)

classes = list(model.named_steps["model"].classes_)

cm = confusion_matrix(
    y_test,
    predictions,
    labels=classes,
)

pd.DataFrame(
    cm,
    index=classes,
    columns=classes,
).to_csv(
    RESULTS_DIR / "gp_confusion_matrix.csv"
)

metrics = {
    "dataset": "Synthetic educational GP symptom dataset",
    "dataset_size": int(len(df)),
    "train_size": int(len(X_train)),
    "test_size": int(len(X_test)),
    "features": FEATURES,
    "classes": classes,
    "accuracy": float(accuracy),
    "macro_f1": float(macro_f1),
    "classification_report": report,
    "limitations": (
        "Synthetic educational dataset generated from clinically "
        "plausible symptom patterns. This model is not clinically "
        "validated and must not be used for real patient care."
    ),
}

with open(
    RESULTS_DIR / "gp_metrics.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(metrics, f, indent=2)

joblib.dump(
    model,
    MODEL_DIR / "gp_disease_model.joblib",
)

metadata = {
    "model_name": "iHIS GP Multiclass Logistic Regression",
    "version": "1.0",
    "features": FEATURES,
    "classes": classes,
    "dataset": "gp_week2_synthetic.csv",
    "dataset_type": "Synthetic educational healthcare dataset",
    "accuracy": float(accuracy),
    "macro_f1": float(macro_f1),
}

with open(
    MODEL_DIR / "gp_disease_model_metadata.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(metadata, f, indent=2)

print("Dataset:", dataset_path)
print("Samples:", len(df))
print("Classes:", classes)
print("Accuracy:", round(accuracy, 3))
print("Macro F1:", round(macro_f1, 3))
print("Model saved:", MODEL_DIR / "gp_disease_model.joblib")
