from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image

import torch
from torch import nn


ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    ROOT
    / "model_artifacts"
    / "radiologist_cnn.pt"
)

CLASSES = [
    "Normal",
    "Pneumonia",
    "Possible fracture",
]


class XRayCNN(nn.Module):
    """Week 4 educational convolutional neural network."""

    def __init__(self):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(
                1,
                8,
                kernel_size=3,
                padding=1,
            ),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(
                8,
                16,
                kernel_size=3,
                padding=1,
            ),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(
                16,
                32,
                kernel_size=3,
                padding=1,
            ),
            nn.ReLU(),

            nn.AdaptiveAvgPool2d(
                (4, 4)
            ),
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),

            nn.Linear(
                32 * 4 * 4,
                64,
            ),
            nn.ReLU(),

            nn.Linear(
                64,
                len(CLASSES),
            ),
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Radiologist CNN model not found. "
            "Run scripts/train_imaging_model.py first."
        )

    model = XRayCNN()

    state_dict = torch.load(
        MODEL_PATH,
        map_location="cpu",
    )

    model.load_state_dict(
        state_dict
    )

    model.eval()

    return model


def preprocess_image(path):
    image = Image.open(
        path
    ).convert("L")

    image = image.resize(
        (64, 64)
    )

    array = np.asarray(
        image,
        dtype=np.float32,
    ) / 255.0

    tensor = (
        torch.from_numpy(array)
        .unsqueeze(0)
        .unsqueeze(0)
    )

    return tensor


def analyze_xray(path):
    """
    Analyze an uploaded educational X-ray using a real CNN.

    The model is trained only on synthetic demonstration images.
    """

    model = load_model()

    tensor = preprocess_image(
        path
    )

    with torch.no_grad():
        logits = model(
            tensor
        )

        probabilities = torch.softmax(
            logits,
            dim=1,
        )[0]

    ranked_indices = torch.argsort(
        probabilities,
        descending=True,
    ).tolist()

    ranked = [
        (
            CLASSES[index],
            float(
                probabilities[index].item()
            ),
        )
        for index in ranked_indices
    ]

    prediction = ranked[0][0]

    if prediction == "Pneumonia":
        interpretation = (
            "The educational CNN detected a "
            "pneumonia-like opacity pattern."
        )

    elif prediction == "Possible fracture":
        interpretation = (
            "The educational CNN detected a "
            "fracture-like linear pattern."
        )

    else:
        interpretation = (
            "The educational CNN did not detect "
            "the predefined pneumonia-like or "
            "fracture-like synthetic patterns."
        )

    return {
        "prediction": prediction,

        "score": float(
            ranked[0][1]
        ),

        "ranked_predictions": [
            {
                "label": label,
                "probability": probability,
            }
            for label, probability in ranked
        ],

        "interpretation": interpretation,

        "model_name": (
            "iHIS Educational Radiologist CNN"
        ),

        "model_version": "2.0",

        "algorithm": (
            "Convolutional Neural Network (CNN)"
        ),

        "framework": "PyTorch",

        "architecture": (
            "Three convolutional layers with "
            "ReLU activation, pooling and a "
            "fully connected classifier."
        ),

        "disclaimer": (
            "Educational deep-learning prototype only. "
            "The CNN was trained on synthetic X-ray-like "
            "images and is not clinically validated for "
            "radiological diagnosis."
        ),
    }
