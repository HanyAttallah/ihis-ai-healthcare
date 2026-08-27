MODEL_NAME = "iHIS Mental Health Screening Engine"
MODEL_VERSION = "1.0"


def interpret_score(score):
    if score >= 3:
        return "Positive screening threshold"

    return "Below screening threshold"


def analyze_mental_health(
    low_interest,
    depressed_mood,
    nervous,
    unable_to_stop_worrying,
):
    """
    Educational PHQ-2 / GAD-2 style screening.

    Screening only; this function does not establish
    a psychiatric diagnosis.
    """

    depression_score = (
        int(low_interest)
        + int(depressed_mood)
    )

    anxiety_score = (
        int(nervous)
        + int(unable_to_stop_worrying)
    )

    depression_result = interpret_score(
        depression_score
    )

    anxiety_result = interpret_score(
        anxiety_score
    )

    recommendations = []

    if depression_score >= 3:
        recommendations.append(
            "Positive depression screening threshold. "
            "Consider fuller clinical assessment."
        )

    if anxiety_score >= 3:
        recommendations.append(
            "Positive anxiety screening threshold. "
            "Consider fuller clinical assessment."
        )

    if (
        depression_score < 3
        and anxiety_score < 3
    ):
        recommendations.append(
            "Scores are below the predefined screening threshold."
        )

    recommendations.append(
        "Urgent professional assessment is required "
        "if there is immediate safety concern or risk of harm."
    )

    return {
        "depression_score": depression_score,
        "depression_result": depression_result,
        "anxiety_score": anxiety_score,
        "anxiety_result": anxiety_result,
        "recommendations": recommendations,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "disclaimer": (
            "Educational mental-health screening prototype only. "
            "It does not diagnose depression or anxiety."
        ),
    }
