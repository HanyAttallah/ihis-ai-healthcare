from pathlib import Path
import json

import numpy as np
from PIL import Image
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


ROOT = Path(__file__).resolve().parents[1]

MODEL_DIR = ROOT / "model_artifacts"
RESULTS_DIR = ROOT / "docs" / "deliverables" / "week_04" / "results"
DEMO_DIR = ROOT / "data" / "week4_demo"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
DEMO_DIR.mkdir(parents=True, exist_ok=True)

CLASSES = [
    "Normal",
    "Pneumonia",
    "Possible fracture",
]

IMAGE_SIZE = 64

np.random.seed(42)
torch.manual_seed(42)


class XRayCNN(nn.Module):
    """
    Small educational convolutional neural network.

    This CNN is intentionally compact so that the Week 4 model can
    be trained on CPU and reproduced during project assessment.
    """

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


def create_base_xray(label, seed=None):
    """
    Create a synthetic educational X-ray-like grayscale image.

    These images are not patient radiographs and are used only to
    demonstrate the deep-learning workflow required by the project.
    """

    local_rng = np.random.default_rng(seed)

    size = IMAGE_SIZE
    y, x = np.ogrid[:size, :size]

    image = np.full(
        (size, size),
        0.42,
        dtype=np.float32,
    )

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

    # Mediastinum.
    image[:, 29:35] += 0.12

    # Rib-like structures.
    for row in range(12, 56, 8):
        image[
            row:row + 1,
            8:56,
        ] += 0.06

    image += local_rng.normal(
        0,
        0.025,
        image.shape,
    )

    if label == "Pneumonia":
        side = local_rng.choice(
            ["left", "right"]
        )

        cx = (
            21
            if side == "left"
            else 43
        )

        cy = int(
            local_rng.integers(
                38,
                48,
            )
        )

        opacity = (
            ((x - cx) / 10) ** 2
            + ((y - cy) / 9) ** 2
            <= 1
        )

        image[
            opacity & lungs
        ] += float(
            local_rng.uniform(
                0.22,
                0.34,
            )
        )

    elif label == "Possible fracture":
        start_x = int(
            local_rng.integers(
                8,
                18,
            )
        )

        start_y = int(
            local_rng.integers(
                15,
                28,
            )
        )

        slope = float(
            local_rng.uniform(
                0.45,
                0.8,
            )
        )

        for dx in range(30):
            px = start_x + dx
            py = int(
                start_y
                + slope * dx
            )

            if (
                1 <= px < 63
                and 1 <= py < 63
            ):
                image[
                    py - 1:py + 2,
                    px - 1:px + 2,
                ] += 0.32

    return np.clip(
        image,
        0,
        1,
    ).astype(np.float32)


images = []
labels = []

for class_index, label in enumerate(
    CLASSES
):
    for sample_index in range(300):
        image = create_base_xray(
            label,
            seed=(
                class_index * 10000
                + sample_index
            ),
        )

        images.append(image)
        labels.append(class_index)


X = np.asarray(
    images,
    dtype=np.float32,
)

y = np.asarray(
    labels,
    dtype=np.int64,
)


X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )
)


X_train_tensor = (
    torch.from_numpy(X_train)
    .unsqueeze(1)
)

y_train_tensor = (
    torch.from_numpy(y_train)
)

X_test_tensor = (
    torch.from_numpy(X_test)
    .unsqueeze(1)
)

y_test_tensor = (
    torch.from_numpy(y_test)
)


train_loader = DataLoader(
    TensorDataset(
        X_train_tensor,
        y_train_tensor,
    ),
    batch_size=32,
    shuffle=True,
)


model = XRayCNN()

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001,
)


EPOCHS = 18

for epoch in range(EPOCHS):
    model.train()

    running_loss = 0.0

    for batch_x, batch_y in train_loader:
        optimizer.zero_grad()

        logits = model(batch_x)

        loss = criterion(
            logits,
            batch_y,
        )

        loss.backward()
        optimizer.step()

        running_loss += (
            loss.item()
            * batch_x.size(0)
        )

    epoch_loss = (
        running_loss
        / len(train_loader.dataset)
    )

    print(
        f"Epoch {epoch + 1:02d}/{EPOCHS} "
        f"- loss: {epoch_loss:.4f}"
    )


model.eval()

with torch.no_grad():
    logits = model(
        X_test_tensor
    )

    probabilities = torch.softmax(
        logits,
        dim=1,
    )

    predictions = torch.argmax(
        probabilities,
        dim=1,
    ).cpu().numpy()


accuracy = accuracy_score(
    y_test,
    predictions,
)

report = classification_report(
    y_test,
    predictions,
    target_names=CLASSES,
    output_dict=True,
    zero_division=0,
)


MODEL_PATH = (
    MODEL_DIR
    / "radiologist_cnn.pt"
)

torch.save(
    model.state_dict(),
    MODEL_PATH,
)


metrics = {
    "dataset_type": (
        "Synthetic educational X-ray-like image dataset"
    ),
    "samples": int(len(X)),
    "train_samples": int(len(X_train)),
    "test_samples": int(len(X_test)),
    "classes": CLASSES,
    "algorithm": (
        "Convolutional Neural Network (CNN)"
    ),
    "framework": "PyTorch",
    "architecture": [
        "Conv2d 1->8 + ReLU + MaxPool",
        "Conv2d 8->16 + ReLU + MaxPool",
        "Conv2d 16->32 + ReLU",
        "AdaptiveAvgPool2d 4x4",
        "Dense 512->64 + ReLU",
        "Dense 64->3",
    ],
    "epochs": EPOCHS,
    "accuracy": float(accuracy),
    "classification_report": report,
    "limitations": (
        "Synthetic educational image dataset only. "
        "Performance does not represent clinical validation "
        "and the model must not be used for patient diagnosis."
    ),
}


with open(
    RESULTS_DIR
    / "radiologist_metrics.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        metrics,
        f,
        indent=2,
    )


for index, label in enumerate(
    CLASSES
):
    demo = create_base_xray(
        label,
        seed=90000 + index,
    )

    filename = (
        label.lower()
        .replace(" ", "_")
        + ".png"
    )

    Image.fromarray(
        (demo * 255).astype(
            np.uint8
        )
    ).save(
        DEMO_DIR / filename
    )


print()
print(
    "CNN model:",
    MODEL_PATH,
)
print(
    "Held-out accuracy:",
    round(accuracy, 4),
)
print(
    "Algorithm: Convolutional Neural Network (CNN)"
)
