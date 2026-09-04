from functools import lru_cache
from pathlib import Path
from zipfile import ZipFile

import numpy as np
from PIL import Image


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

# The frozen .pt artifact is a PyTorch state_dict ZIP archive.  The public
# educational deployment has only 256 MB RAM, while importing PyTorch alone
# can exceed that limit.  These tensor specifications allow inference from the
# exact trained CNN weights with NumPy, without importing the PyTorch runtime.
# The submitted/frozen main branch remains the genuine PyTorch implementation.
TENSOR_SPECS = {
    "features.0.weight": ("0", (8, 1, 3, 3)),
    "features.0.bias": ("1", (8,)),
    "features.3.weight": ("2", (16, 8, 3, 3)),
    "features.3.bias": ("3", (16,)),
    "features.6.weight": ("4", (32, 16, 3, 3)),
    "features.6.bias": ("5", (32,)),
    "classifier.1.weight": ("6", (64, 512)),
    "classifier.1.bias": ("7", (64,)),
    "classifier.3.weight": ("8", (3, 64)),
    "classifier.3.bias": ("9", (3,)),
}


@lru_cache(maxsize=1)
def load_model():
    """Load the frozen PyTorch CNN weights without importing torch."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Radiologist CNN model not found. "
            "Run scripts/train_imaging_model.py in the full development "
            "environment first."
        )

    with ZipFile(MODEL_PATH) as archive:
        names = archive.namelist()

        storage_zero = next(
            (
                name
                for name in names
                if name.endswith("/data/0")
            ),
            None,
        )

        if storage_zero is None:
            raise RuntimeError(
                "Unsupported radiologist CNN artifact format."
            )

        archive_root = storage_zero.rsplit(
            "/data/",
            1,
        )[0]

        byteorder_name = (
            f"{archive_root}/byteorder"
        )

        byteorder = "little"
        if byteorder_name in names:
            byteorder = (
                archive.read(byteorder_name)
                .decode("ascii")
                .strip()
            )

        dtype = (
            "<f4"
            if byteorder == "little"
            else ">f4"
        )

        weights = {}

        for (
            key,
            (storage_id, shape),
        ) in TENSOR_SPECS.items():
            raw = archive.read(
                f"{archive_root}/data/{storage_id}"
            )

            array = np.frombuffer(
                raw,
                dtype=dtype,
            ).astype(
                np.float32,
                copy=True,
            )

            expected_size = int(
                np.prod(shape)
            )

            if array.size != expected_size:
                raise RuntimeError(
                    "Unexpected tensor size in radiologist CNN artifact."
                )

            weights[key] = array.reshape(
                shape
            )

    return weights


def _conv2d_same(
    tensor,
    weight,
    bias,
):
    padded = np.pad(
        tensor,
        (
            (0, 0),
            (1, 1),
            (1, 1),
        ),
        mode="constant",
    )

    windows = (
        np.lib.stride_tricks
        .sliding_window_view(
            padded,
            (3, 3),
            axis=(1, 2),
        )
    )

    output = np.einsum(
        "chwkl,ockl->ohw",
        windows,
        weight,
        optimize=True,
    )

    return (
        output
        + bias[:, None, None]
    )


def _max_pool_2x2(tensor):
    channels, height, width = (
        tensor.shape
    )

    return tensor.reshape(
        channels,
        height // 2,
        2,
        width // 2,
        2,
    ).max(
        axis=(2, 4)
    )


def _adaptive_avg_pool_4x4(tensor):
    channels, height, width = (
        tensor.shape
    )

    if (
        height % 4 != 0
        or width % 4 != 0
    ):
        raise RuntimeError(
            "Unexpected CNN feature-map size."
        )

    return tensor.reshape(
        channels,
        4,
        height // 4,
        4,
        width // 4,
    ).mean(
        axis=(2, 4)
    )


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

    return array[
        None,
        :,
        :,
    ]


def _predict_probabilities(path):
    weights = load_model()

    tensor = preprocess_image(
        path
    )

    tensor = np.maximum(
        _conv2d_same(
            tensor,
            weights[
                "features.0.weight"
            ],
            weights[
                "features.0.bias"
            ],
        ),
        0.0,
    )

    tensor = _max_pool_2x2(
        tensor
    )

    tensor = np.maximum(
        _conv2d_same(
            tensor,
            weights[
                "features.3.weight"
            ],
            weights[
                "features.3.bias"
            ],
        ),
        0.0,
    )

    tensor = _max_pool_2x2(
        tensor
    )

    tensor = np.maximum(
        _conv2d_same(
            tensor,
            weights[
                "features.6.weight"
            ],
            weights[
                "features.6.bias"
            ],
        ),
        0.0,
    )

    tensor = (
        _adaptive_avg_pool_4x4(
            tensor
        )
        .reshape(-1)
    )

    hidden = np.maximum(
        (
            weights[
                "classifier.1.weight"
            ]
            @ tensor
            + weights[
                "classifier.1.bias"
            ]
        ),
        0.0,
    )

    logits = (
        weights[
            "classifier.3.weight"
        ]
        @ hidden
        + weights[
            "classifier.3.bias"
        ]
    )

    shifted = (
        logits
        - np.max(logits)
    )

    exponentials = np.exp(
        shifted
    )

    return (
        exponentials
        / exponentials.sum()
    )


def analyze_xray(path):
    """
    Analyze an uploaded educational X-ray using the trained CNN weights.

    The underlying model is the genuine Week 4 PyTorch CNN trained on
    synthetic demonstration images.  The public low-memory deployment executes
    the frozen trained weights with an equivalent NumPy inference path so that
    the educational site can run within the free-host memory limit.
    """

    probabilities = (
        _predict_probabilities(
            path
        )
    )

    ranked_indices = np.argsort(
        probabilities
    )[::-1].tolist()

    ranked = [
        (
            CLASSES[index],
            float(
                probabilities[index]
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

        "framework": (
            "PyTorch-trained CNN; NumPy inference "
            "runtime for the public low-memory demo"
        ),

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
