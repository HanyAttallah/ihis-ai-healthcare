from flask import render_template

from app.auth.decorators import roles_required
from app.emergency import bp
from app.emergency.forms import EmergencyBFSForm
from app.extensions import db
from app.models import Patient
from app.services.ai.emergency_bfs import (
    bfs_emergency_reasoning,
)


@bp.route(
    "/patients/<int:patient_id>/bfs",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
    "Nurse",
)
def bfs_assessment(patient_id):
    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    form = EmergencyBFSForm()
    result = None

    if form.validate_on_submit():
        names = [
            "chest_pain",
            "dyspnea",
            "sweating",
            "nausea",
            "tachycardia",
            "hemoptysis",
            "wheeze",
            "chest_tightness",
            "sudden_weakness",
            "speech_difficulty",
            "seizure",
            "altered_consciousness",
            "fever",
            "hypotension",
            "rash",
            "swelling",
        ]

        symptoms = {
            name: bool(
                getattr(form, name).data
            )
            for name in names
        }

        result = bfs_emergency_reasoning(
            symptoms
        )

    return render_template(
        "emergency/bfs.html",
        patient=patient,
        form=form,
        result=result,
    )
