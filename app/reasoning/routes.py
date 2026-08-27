from flask import render_template

from app.auth.decorators import roles_required
from app.extensions import db
from app.models import Patient
from app.reasoning import bp
from app.reasoning.forms import ClinicalReasoningForm
from app.services.ai.clinical_reasoning import (
    reason_from_symptoms,
)


@bp.route(
    "/patients/<int:patient_id>/differential",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
)
def differential(patient_id):
    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    form = ClinicalReasoningForm()
    result = None

    if form.validate_on_submit():
        symptom_data = {
            name: bool(
                getattr(form, name).data
            )
            for name in [
                "fever",
                "cough",
                "sputum",
                "dyspnea",
                "chest_pain",
                "sore_throat",
                "nasal_symptoms",
                "fatigue",
                "dysuria",
                "urinary_frequency",
                "lower_abdominal_pain",
                "abdominal_pain",
                "diarrhea",
                "vomiting",
                "nausea",
                "sweating",
                "wheeze",
                "chest_tightness",
            ]
        }

        result = reason_from_symptoms(
            symptom_data
        )

    return render_template(
        "reasoning/differential.html",
        patient=patient,
        form=form,
        result=result,
    )
