from flask import render_template, request

from app.auth.decorators import roles_required
from app.extensions import db
from app.gp import bp
from app.gp.forms import GPConsultationForm
from app.models import Patient
from app.services.ai.gp_disease import predict_gp_case


@bp.route(
    "/patients/<int:patient_id>/consultation",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
)
def consultation(patient_id):
    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    form = GPConsultationForm()
    result = None

    if request.method == "GET" and patient.age is not None:
        form.age.data = patient.age

    if form.validate_on_submit():
        result = predict_gp_case(
            {
                "age": form.age.data,
                "temperature": float(
                    form.temperature.data
                ),
                "heart_rate": form.heart_rate.data,
                "cough": form.cough.data,
                "sputum": form.sputum.data,
                "dyspnea": form.dyspnea.data,
                "dysuria": form.dysuria.data,
                "urinary_frequency": (
                    form.urinary_frequency.data
                ),
                "abdominal_pain": (
                    form.abdominal_pain.data
                ),
                "diarrhea": form.diarrhea.data,
                "vomiting": form.vomiting.data,
                "smoking": form.smoking.data,
            }
        )

    return render_template(
        "gp/consultation.html",
        patient=patient,
        form=form,
        result=result,
    )
