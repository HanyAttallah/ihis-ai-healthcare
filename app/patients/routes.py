from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.auth.decorators import roles_required
from app.extensions import db
from app.models import Encounter, Patient
from app.patients import bp
from app.patients.forms import PatientRegistrationForm
from app.services.mrn import generate_mrn


@bp.route("/")
@roles_required(
    "Administrator",
    "Receptionist",
    "Doctor",
    "Nurse",
)
def index():
    """Display and search the iHIS Patient Registry."""

    query = request.args.get("q", "").strip()

    statement = db.select(Patient)

    if query:
        pattern = f"%{query}%"

        statement = statement.where(
            db.or_(
                Patient.mrn.ilike(pattern),
                Patient.first_name.ilike(pattern),
                Patient.middle_name.ilike(pattern),
                Patient.last_name.ilike(pattern),
            )
        )

    statement = statement.order_by(
        Patient.last_name,
        Patient.first_name,
        Patient.id,
    )

    patients = db.session.execute(
        statement
    ).scalars().all()

    return render_template(
        "patients/index.html",
        patients=patients,
        query=query,
    )


@bp.route("/register", methods=["GET", "POST"])
@roles_required("Administrator", "Receptionist")
def register():
    """Register a new patient in the iHIS Patient Registry."""

    form = PatientRegistrationForm()

    if form.validate_on_submit():
        patient = Patient(
            mrn=generate_mrn(),
            first_name=form.first_name.data.strip(),
            middle_name=(
                form.middle_name.data.strip()
                if form.middle_name.data
                else None
            ),
            last_name=form.last_name.data.strip(),
            date_of_birth=form.date_of_birth.data,
            sex=form.sex.data,
            phone=(
                form.phone.data.strip()
                if form.phone.data
                else None
            ),
            email=(
                form.email.data.strip().lower()
                if form.email.data
                else None
            ),
            address=(
                form.address.data.strip()
                if form.address.data
                else None
            ),
            emergency_contact_name=(
                form.emergency_contact_name.data.strip()
                if form.emergency_contact_name.data
                else None
            ),
            emergency_contact_phone=(
                form.emergency_contact_phone.data.strip()
                if form.emergency_contact_phone.data
                else None
            ),
            created_by_id=current_user.id,
        )

        db.session.add(patient)
        db.session.commit()

        flash(
            f"Patient registered successfully. MRN: {patient.mrn}",
            "success",
        )

        return redirect(
            url_for(
                "patients.profile",
                patient_id=patient.id,
            )
        )

    return render_template(
        "patients/register.html",
        form=form,
    )


@bp.route("/<int:patient_id>")
@roles_required(
    "Administrator",
    "Receptionist",
    "Doctor",
    "Nurse",
)
def profile(patient_id):
    """Display patient demographics and longitudinal encounter history."""

    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    encounters = db.session.execute(
        db.select(Encounter)
        .where(Encounter.patient_id == patient.id)
        .order_by(
            Encounter.started_at.desc(),
            Encounter.id.desc(),
        )
    ).scalars().all()

    return render_template(
        "patients/profile.html",
        patient=patient,
        encounters=encounters,
    )
