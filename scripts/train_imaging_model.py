from pathlib import Path
import json

import joblib
import numpy as np
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]

MODEL_DIR = ROOT / "model_artifacts"
RESULTS_DIR = ROOT / "docs" / "deliverables" / "week_04" / "results"
DEMO_DIR = ROOT / "data" / "week4_demo"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
DEMO_DIR.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(42)

CLASSES = [
    "Normal",
    "Pneumonia",
    "Possible fracture",
]


def create_base_xray(label, seed=None):
    local_rng = np.random.default_rng(seed)

    size = 64
    y, x = np.ogrid[:size, :size]

    image = np.full(
        (size, size),
        0.42,
        dtype=np.float32,
    )

    # Two synthetic lung fields.
    left_lung = (
        ((x - 21) / 13) ** 2
        + ((y - 34) / 24) ** 2
        <= 1
    )

    right_lung = (
        ((x - 43) / 13) ** 2
        + ((y - 34) / 24) ** 2
        <= 1
    )

    lungs = left_lung | right_lung
    image[lungs] = 0.20

    # Mediastinal region.
    image[:, 29:35] += 0.12

    # Mild rib-like horizontal structures.
    for row in range(12, 56, 8):
        image[row:row + 1, 8:56] += 0.06

    image += local_rng.normal(
        0,
        0.025,
        image.shape,
    )

    if label == "Pneumonia":
        side = local_rng.choice(["left", "right"])
        cx = 21 if side == "left" else 43
        cy = int(local_rng.integers(38, 48))

        opacity = (
            ((x - cx) / 10) ** 2
            + ((y - cy) / 9) ** 2
            <= 1
        )

        image[opacity & lungs] += float(
            local_rng.uniform(0.22, 0.34)
        )

    elif label == "Possible fracture":
        start_x = int(local_rng.integers(8, 18))
        start_y = int(local_rng.integers(15, 28))
        slope = float(local_rng.uniform(0.45, 0.8))

        for dx in range(30):
            px = start_x + dx
            py = int(start_y + slope * dx)

            if 1 <= px < 63 and 1 <= py < 63:
                image[
                    py - 1:py + 2,
                    px - 1:px + 2
                ] += 0.32

    image = np.clip(
        image,
        0,
        1,
    )

    return image


def extract_features(image_array):
    image = Image.fromarray(
        (image_array * 255).astype(np.uint8)
    )

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


X = []
y = []

for class_index, label in enumerate(CLASSES):
    for i in range(300):
        image = create_base_xray(
            label,
            seed=class_index * 10000 + i,
        )

        X.append(
            extract_features(image)
        )

        y.append(label)

X = np.asarray(X)
y = np.asarray(y)

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
                max_iter=1500,
                random_state=42,
            ),
        ),
    ]
)

model.fit(
    X_train,
    y_train,
)

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions,
)

report = classification_report(
    y_test,
    predictions,
    output_dict=True,
)

joblib.dump(
    model,
    MODEL_DIR / "radiologist_xray_model.joblib",
)

metrics = {
    "dataset_type": (
        "Synthetic educational X-ray-like image dataset"
    ),
    "samples": int(len(X)),
    "classes": CLASSES,
    "accuracy": float(accuracy),
    "classification_report": report,
    "limitations": (
        "Synthetic educational image dataset only. "
        "Performance does not represent clinical validation."
    ),
}

with open(
    RESULTS_DIR / "radiologist_metrics.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        metrics,
        f,
        indent=2,
    )

# Save three demonstration images.
for index, label in enumerate(CLASSES):
    demo = create_base_xray(
        label,
        seed=90000 + index,
    )

    Image.fromarray(
        (demo * 255).astype(np.uint8)
    ).save(
        DEMO_DIR
        / (
            label.lower()
            .replace(" ", "_")
            + ".png"
        )
    )

print("Synthetic image samples:", len(X))
print("Classes:", CLASSES)
print("Held-out accuracy:", round(accuracy, 3))
print(
    "Model:",
    MODEL_DIR / "radiologist_xray_model.joblib",
)
print("Demo images:", DEMO_DIR)
