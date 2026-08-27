from pathlib import Path

import pytest

from app.services.ai.radiologist import analyze_xray
from app.services.ai.icu_cdss import analyze_icu_vitals
from app.services.ai.multi_agent import (
    ALL_SPECIALISTS,
    SCENARIOS,
    select_relevant_agents,
)

import app.services.ai.patient_education as patient_education


def test_week4_cnn_inference():
    """Week 4 must use the trained CNN for image inference."""

    image_path = Path(
        "data/week4_demo/pneumonia.png"
    )

    assert image_path.exists()

    result = analyze_xray(
        image_path
    )

    assert (
        result["algorithm"]
        == "Convolutional Neural Network (CNN)"
    )

    assert (
        result["prediction"]
        == "Pneumonia"
    )

    assert (
        0.0
        <= result["score"]
        <= 1.0
    )


def test_week5_rag_retrieval_and_llm_contract(
    monkeypatch,
):
    """
    Week 5 must retrieve local evidence and pass it
    to a generator.

    The external Groq API is mocked here so pytest
    remains deterministic and does not require network
    access or consume API quota.
    """

    question = (
        "What should a patient know about pneumonia?"
    )

    retrieved = (
        patient_education.retrieve_context(
            question
        )
    )

    assert len(retrieved) >= 1
    assert (
        retrieved[0]["retrieval_score"]
        > 0
    )

    def fake_generator(
        supplied_question,
        supplied_context,
    ):
        assert (
            supplied_question
            == question
        )

        assert (
            len(supplied_context)
            >= 1
        )

        return (
            "Grounded synthetic test answer.",
            "test-generator",
        )

    monkeypatch.setattr(
        patient_education,
        "generate_grounded_answer",
        fake_generator,
    )

    result = (
        patient_education.answer_patient_question(
            question
        )
    )

    assert (
        result["generation_status"]
        == (
            "LLM-generated answer grounded "
            "in retrieved local sources"
        )
    )

    assert (
        result["answer"]
        == "Grounded synthetic test answer."
    )

    assert len(
        result["sources"]
    ) >= 1

    assert (
        result["provider"]
        == "Groq"
    )


@pytest.mark.parametrize(
    "scenario,expected_selected,expected_skipped",
    [
        (
            "respiratory",
            {
                "Receptionist AI",
                "GP AI",
                "Radiologist AI",
                "Clinical Reasoning AI",
                "Clinical Pharmacist AI",
                "Patient Education AI",
            },
            {
                "ICU AI",
                "Emergency AI",
                "Psychiatrist AI",
                "Oncologist AI",
                "Treatment Planning AI",
            },
        ),
        (
            "emergency",
            {
                "Receptionist AI",
                "ICU AI",
                "Emergency AI",
            },
            {
                "GP AI",
                "Radiologist AI",
                "Clinical Reasoning AI",
                "Clinical Pharmacist AI",
                "Psychiatrist AI",
                "Oncologist AI",
                "Treatment Planning AI",
                "Patient Education AI",
            },
        ),
        (
            "mental_health",
            {
                "Receptionist AI",
                "Psychiatrist AI",
            },
            {
                "GP AI",
                "ICU AI",
                "Radiologist AI",
                "Clinical Reasoning AI",
                "Emergency AI",
                "Clinical Pharmacist AI",
                "Oncologist AI",
                "Treatment Planning AI",
                "Patient Education AI",
            },
        ),
        (
            "oncology",
            {
                "Receptionist AI",
                "Oncologist AI",
                "Treatment Planning AI",
            },
            {
                "GP AI",
                "ICU AI",
                "Radiologist AI",
                "Clinical Reasoning AI",
                "Emergency AI",
                "Clinical Pharmacist AI",
                "Psychiatrist AI",
                "Patient Education AI",
            },
        ),
    ],
)
def test_week12_relevance_selection(
    scenario,
    expected_selected,
    expected_skipped,
):
    """Week 12 must select only relevant specialists."""

    selected, _ = (
        select_relevant_agents(
            SCENARIOS[scenario]
        )
    )

    skipped = {
        agent
        for agent in ALL_SPECIALISTS
        if agent not in selected
    }

    assert set(
        selected
    ) == expected_selected

    assert (
        skipped
        == expected_skipped
    )


def test_icu_temperature_encoding():
    """Temperature output must use a proper degree symbol."""

    result = analyze_icu_vitals({
        "temperature": 39.0,
        "heart_rate": 80,
        "respiratory_rate": 16,
        "systolic_bp": 120,
        "oxygen_saturation": 98,
    })

    temperature_alerts = [
        alert
        for alert in result["alerts"]
        if (
            alert["parameter"]
            == "Temperature"
        )
    ]

    assert len(
        temperature_alerts
    ) == 1

    assert (
        temperature_alerts[0]["value"]
        == "39.0 \u00b0C"
    )
