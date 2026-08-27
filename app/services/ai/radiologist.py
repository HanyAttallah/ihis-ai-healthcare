from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    ROOT
    / "model_artifacts"
    / "radiologist_xray_model.joblib"
)


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Radiologist model not found. "
            "Run scripts/train_imaging_model.py first."
        )

    return joblib.load(
        MODEL_PATH
    )


def extract_features_from_path(path):
    image = Image.open(
        path
    ).convert("L")

    image = image.resize(
        (32, 32)
    )

    arr = np.asarray(
        image,
        dtype=np.float32,
    ) / 255.0

    flat = arr.flatten()

    horizontal_edges = np.abs(
        np.diff(arr, axis=1)
    ).mean()

    vertical_edges = np.abs(
        np.diff(arr, axis=0)
    ).mean()

    summary = np.array(
        [
            arr.mean(),
            arr.std(),
            horizontal_edges,
            vertical_edges,
            np.mean(arr > 0.55),
            np.mean(arr < 0.20),
        ],
        dtype=np.float32,
    )

    return np.concatenate(
        [flat, summary]
    )


def analyze_xray(path):
    model = load_model()

    features = extract_features_from_path(
        path
    ).reshape(1, -1)

    probabilities = model.predict_proba(
        features
    )[0]

    classes = model.named_steps[
        "model"
    ].classes_

    ranked = sorted(
        zip(
            classes,
            probabilities,
        ),
        key=lambda item: item[1],
        reverse=True,
    )

    prediction = ranked[0][0]

    if prediction == "Pneumonia":
        interpretation = (
            "The educational image classifier detected "
            "a pneumonia-like opacity pattern."
        )

    elif prediction == "Possible fracture":
        interpretation = (
            "The educational image classifier detected "
            "a fracture-like linear pattern."
        )

    else:
        interpretation = (
            "No pneumonia-like or fracture-like synthetic "
            "pattern was detected by this prototype."
        )

    return {
        "prediction": prediction,
        "score": float(
            ranked[0][1]
        ),
        "ranked_predictions": [
            {
                "label": label,
                "probability": float(
                    probability
                ),
            }
            for label, probability in ranked
        ],
        "interpretation": interpretation,
        "model_name": (
            "iHIS Educational Radiologist Image Classifier"
        ),
        "model_version": "1.0",
        "disclaimer": (
            "Educational prototype only. "
            "The classifier was trained on synthetic "
            "X-ray-like images and is not clinically "
            "validated for radiological diagnosis."
        ),
    }
