from flask import render_template

from app.auth.decorators import roles_required
from app.extensions import db
from app.models import Patient
from app.radiation_oncology import bp
from app.radiation_oncology.forms import (
    RadiationToxicityForm,
)
from app.services.ai.radiation_oncology import (
    analyze_rt_toxicity,
)


@bp.route(
    "/patients/<int:patient_id>/toxicity",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
)
def toxicity(patient_id):

    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    form = RadiationToxicityForm()
    result = None

    if form.validate_on_submit():

        result = analyze_rt_toxicity(
            mucositis_oral=form.mucositis_oral.data,
            dermatitis_radiation=(
                form.dermatitis_radiation.data
            ),
            dysphagia=form.dysphagia.data,
            nausea=form.nausea.data,
            vomiting=form.vomiting.data,
            fatigue=form.fatigue.data,
            pain_score=form.pain_score.data,
            weight_loss=form.weight_loss.data,
            fever=form.fever.data,
        )

    return render_template(
        "radiation_oncology/toxicity.html",
        patient=patient,
        form=form,
        result=result,
    )
