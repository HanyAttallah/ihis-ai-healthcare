from flask import render_template

from app.auth.decorators import roles_required
from app.extensions import db
from app.icu import bp
from app.icu.forms import ICUMonitorForm
from app.models import Patient
from app.services.ai.icu_cdss import analyze_icu_vitals


@bp.route(
    "/patients/<int:patient_id>/monitor",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
    "Nurse",
)
def monitor(patient_id):
    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    form = ICUMonitorForm()
    result = None

    if form.validate_on_submit():
        result = analyze_icu_vitals({
            "temperature": float(form.temperature.data),
            "heart_rate": form.heart_rate.data,
            "respiratory_rate": form.respiratory_rate.data,
            "systolic_bp": form.systolic_bp.data,
            "oxygen_saturation": float(
                form.oxygen_saturation.data
            ),
        })

    return render_template(
        "icu/monitor.html",
        patient=patient,
        form=form,
        result=result,
    )
