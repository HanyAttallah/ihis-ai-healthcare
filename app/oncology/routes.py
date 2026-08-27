from flask import render_template

from app.auth.decorators import roles_required
from app.extensions import db
from app.models import Patient
from app.oncology import bp
from app.oncology.forms import (
    OncologyDFSForm,
    TreatmentRLForm,
)
from app.services.ai.oncology_dfs import (
    dfs_oncology_reasoning,
)
from app.services.ai.treatment_rl import (
    optimize_treatment,
)


@bp.route(
    "/patients/<int:patient_id>/dfs",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
)
def dfs_reasoning(patient_id):
    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    form = OncologyDFSForm()
    result = None

    if form.validate_on_submit():
        names = [
            "persistent_cough",
            "hemoptysis",
            "dyspnea",
            "chest_pain",
            "weight_loss",
            "smoking_history",
            "rectal_bleeding",
            "change_bowel_habit",
            "abdominal_pain",
            "anemia",
            "urinary_obstruction",
            "hematuria",
            "bone_pain",
            "elevated_psa",
        ]

        symptoms = {
            name: bool(
                getattr(
                    form,
                    name,
                ).data
            )
            for name in names
        }

        result = dfs_oncology_reasoning(
            symptoms
        )

    return render_template(
        "oncology/dfs.html",
        patient=patient,
        form=form,
        result=result,
    )


@bp.route(
    "/patients/<int:patient_id>/treatment-rl",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
)
def treatment_rl(patient_id):
    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    form = TreatmentRLForm()
    result = None

    if form.validate_on_submit():
        result = optimize_treatment(
            disease_extent=(
                form.disease_extent.data
            ),
            ecog_status=(
                form.ecog_status.data
            ),
        )

    return render_template(
        "oncology/treatment_rl.html",
        patient=patient,
        form=form,
        result=result,
    )


