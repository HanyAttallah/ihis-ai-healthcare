from flask import render_template

from app.auth.decorators import roles_required
from app.extensions import db
from app.models import Patient
from app.pharmacy import bp
from app.pharmacy.forms import MedicationSafetyForm
from app.services.ai.pharmacist import (
    analyze_medication_safety,
)


@bp.route(
    "/patients/<int:patient_id>/medication-safety",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
    "Pharmacist",
)
def medication_safety(patient_id):
    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    form = MedicationSafetyForm()
    result = None

    if form.validate_on_submit():
        result = analyze_medication_safety(
            condition=form.condition.data,
            current_medications=(
                form.current_medications.data
                or ""
            ),
            allergies=(
                form.allergies.data
                or ""
            ),
            renal_impairment=(
                form.renal_impairment.data
            ),
        )

    return render_template(
        "pharmacy/medication_safety.html",
        patient=patient,
        form=form,
        result=result,
    )
