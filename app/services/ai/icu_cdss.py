MODEL_NAME = "iHIS ICU Vital-Sign CDSS"
MODEL_VERSION = "1.0"


def analyze_icu_vitals(data):
    """
    Analyze vital signs using transparent educational threshold rules.

    This module is an educational CDSS prototype and is not a substitute
    for bedside clinical assessment or local ICU escalation protocols.
    """

    alerts = []

    temperature = float(data["temperature"])
    heart_rate = int(data["heart_rate"])
    respiratory_rate = int(data["respiratory_rate"])
    systolic_bp = int(data["systolic_bp"])
    oxygen_saturation = float(data["oxygen_saturation"])

    # Oxygen saturation
    if oxygen_saturation < 90:
        alerts.append({
            "parameter": "Oxygen saturation",
            "value": f"{oxygen_saturation:.1f}%",
            "severity": "Critical",
            "message": "Severe hypoxemia threshold detected.",
        })
    elif oxygen_saturation < 94:
        alerts.append({
            "parameter": "Oxygen saturation",
            "value": f"{oxygen_saturation:.1f}%",
            "severity": "Warning",
            "message": "Low oxygen saturation detected.",
        })

    # Systolic blood pressure
    if systolic_bp < 90:
        alerts.append({
            "parameter": "Systolic blood pressure",
            "value": f"{systolic_bp} mmHg",
            "severity": "Critical",
            "message": "Hypotension threshold detected.",
        })
    elif systolic_bp < 100 or systolic_bp > 180:
        alerts.append({
            "parameter": "Systolic blood pressure",
            "value": f"{systolic_bp} mmHg",
            "severity": "Warning",
            "message": "Abnormal systolic blood pressure detected.",
        })

    # Heart rate
    if heart_rate < 40 or heart_rate > 130:
        alerts.append({
            "parameter": "Heart rate",
            "value": f"{heart_rate} bpm",
            "severity": "Critical",
            "message": "Critical heart-rate threshold detected.",
        })
    elif heart_rate < 50 or heart_rate > 110:
        alerts.append({
            "parameter": "Heart rate",
            "value": f"{heart_rate} bpm",
            "severity": "Warning",
            "message": "Abnormal heart rate detected.",
        })

    # Respiratory rate
    if respiratory_rate < 8 or respiratory_rate > 30:
        alerts.append({
            "parameter": "Respiratory rate",
            "value": f"{respiratory_rate}/min",
            "severity": "Critical",
            "message": "Critical respiratory-rate threshold detected.",
        })
    elif respiratory_rate < 12 or respiratory_rate > 20:
        alerts.append({
            "parameter": "Respiratory rate",
            "value": f"{respiratory_rate}/min",
            "severity": "Warning",
            "message": "Abnormal respiratory rate detected.",
        })

    # Temperature
    if temperature < 35.0 or temperature >= 40.0:
        alerts.append({
            "parameter": "Temperature",
            "value": f"{temperature:.1f} ?C",
            "severity": "Critical",
            "message": "Critical temperature threshold detected.",
        })
    elif temperature < 36.0 or temperature >= 38.5:
        alerts.append({
            "parameter": "Temperature",
            "value": f"{temperature:.1f} ?C",
            "severity": "Warning",
            "message": "Abnormal temperature detected.",
        })

    critical_count = sum(
        1 for alert in alerts
        if alert["severity"] == "Critical"
    )

    warning_count = sum(
        1 for alert in alerts
        if alert["severity"] == "Warning"
    )

    if critical_count:
        status = "Critical"
    elif warning_count:
        status = "Warning"
    else:
        status = "Stable"

    recommendations = []

    if status == "Critical":
        recommendations.extend([
            "Immediate clinician / ICU senior review.",
            "Repeat and verify abnormal observations.",
            "Perform urgent airway, breathing, and circulation assessment.",
            "Escalate according to the local emergency or ICU protocol.",
        ])

    elif status == "Warning":
        recommendations.extend([
            "Prompt clinical reassessment.",
            "Repeat abnormal vital signs and evaluate the trend.",
            "Escalate if abnormalities persist or worsen.",
        ])

    else:
        recommendations.append(
            "Continue routine monitoring and reassess if the clinical condition changes."
        )

    if oxygen_saturation < 94:
        recommendations.append(
            "Assess oxygenation and the need for supplemental oxygen according to local clinical protocol."
        )

    if systolic_bp < 90:
        recommendations.append(
            "Assess perfusion and hemodynamic status urgently."
        )

    if respiratory_rate > 30 or respiratory_rate < 8:
        recommendations.append(
            "Urgently assess respiratory function and ventilatory support requirements."
        )

    return {
        "status": status,
        "alerts": alerts,
        "critical_count": critical_count,
        "warning_count": warning_count,
        "recommendations": recommendations,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "disclaimer": (
            "Educational ICU clinical decision-support prototype only. "
            "Thresholds must not replace bedside assessment, clinician judgment, "
            "or institutional ICU escalation protocols."
        ),
    }
