from flask import render_template

from app.auth.decorators import roles_required
from app.extensions import db
from app.mental_health import bp
from app.mental_health.forms import MentalHealthAssessmentForm
from app.models import Patient
from app.services.ai.mental_health import analyze_mental_health


@bp.route(
    "/patients/<int:patient_id>/assessment",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
)
def assessment(patient_id):
    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    form = MentalHealthAssessmentForm()
    result = None

    if form.validate_on_submit():
        result = analyze_mental_health(
            low_interest=form.low_interest.data,
            depressed_mood=form.depressed_mood.data,
            nervous=form.nervous.data,
            unable_to_stop_worrying=(
                form.unable_to_stop_worrying.data
            ),
        )

    return render_template(
        "mental_health/assessment.html",
        patient=patient,
        form=form,
        result=result,
    )
