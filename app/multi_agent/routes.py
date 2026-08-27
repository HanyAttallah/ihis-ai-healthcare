from flask import render_template

from app.auth.decorators import roles_required
from app.extensions import db
from app.models import Patient
from app.multi_agent import bp
from app.multi_agent.forms import MultiAgentDemoForm
from app.services.ai.multi_agent import run_integrated_case


@bp.route(
    "/patients/<int:patient_id>/integrated-case",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
)
def integrated_case(patient_id):
    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    form = MultiAgentDemoForm()
    result = None

    if form.validate_on_submit():
        result = run_integrated_case()

    return render_template(
        "multi_agent/integrated_case.html",
        patient=patient,
        form=form,
        result=result,
    )
