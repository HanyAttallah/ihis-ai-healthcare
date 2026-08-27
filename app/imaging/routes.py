from pathlib import Path
from uuid import uuid4

from flask import current_app, render_template
from werkzeug.utils import secure_filename

from app.auth.decorators import roles_required
from app.extensions import db
from app.imaging import bp
from app.imaging.forms import XRayUploadForm
from app.models import Patient
from app.services.ai.radiologist import analyze_xray


@bp.route(
    "/patients/<int:patient_id>/xray",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
    "Radiologist",
)
def xray_analysis(patient_id):
    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    form = XRayUploadForm()
    result = None
    filename = None

    if form.validate_on_submit():
        upload_dir = (
            Path(current_app.instance_path)
            / "imaging_uploads"
        )

        upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        original_name = secure_filename(
            form.image.data.filename
        )

        suffix = Path(
            original_name
        ).suffix.lower()

        saved_name = (
            f"{uuid4().hex}{suffix}"
        )

        saved_path = (
            upload_dir / saved_name
        )

        form.image.data.save(
            saved_path
        )

        result = analyze_xray(
            saved_path
        )

        filename = original_name

    return render_template(
        "imaging/xray.html",
        patient=patient,
        form=form,
        result=result,
        filename=filename,
    )
