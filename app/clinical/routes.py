from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from app.auth.decorators import roles_required
from app.clinical import bp
from app.clinical.forms import (
    ChiefComplaintForm,
    ClinicalNoteForm,
    DiagnosisForm,
    EncounterForm,
    InvestigationForm,
    VitalSignForm,
)
from app.extensions import db
from app.models import (
    ChiefComplaint,
    ClinicalNote,
    Diagnosis,
    Encounter,
    Investigation,
    Patient,
    VitalSign,
)


@bp.route(
    "/patients/<int:patient_id>/encounters/new",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Receptionist",
    "Doctor",
    "Nurse",
)
def start_encounter(patient_id):
    """Start a new clinical encounter for a registered patient."""

    patient = db.get_or_404(Patient, patient_id)
    form = EncounterForm()

    if form.validate_on_submit():
        encounter = Encounter(
            patient_id=patient.id,
            encounter_type=form.encounter_type.data,
            department=(
                form.department.data.strip()
                if form.department.data
                else None
            ),
            presenting_complaint=(
                form.presenting_complaint.data.strip()
                if form.presenting_complaint.data
                else None
            ),
            created_by_id=current_user.id,
        )

        db.session.add(encounter)
        db.session.commit()

        flash(
            f"Encounter #{encounter.id} started successfully.",
            "success",
        )

        return redirect(
            url_for(
                "clinical.encounter_detail",
                encounter_id=encounter.id,
            )
        )

    return render_template(
        "clinical/start_encounter.html",
        patient=patient,
        form=form,
    )


@bp.route("/encounters/<int:encounter_id>")
@roles_required(
    "Administrator",
    "Receptionist",
    "Doctor",
    "Nurse",
)
def encounter_detail(encounter_id):
    """Display one clinical encounter."""

    encounter = db.get_or_404(
        Encounter,
        encounter_id,
    )

    chief_complaints = db.session.execute(
        db.select(ChiefComplaint)
        .where(
            ChiefComplaint.encounter_id == encounter.id
        )
        .order_by(
            ChiefComplaint.recorded_at.desc(),
            ChiefComplaint.id.desc(),
        )
    ).scalars().all()

    vital_signs = db.session.execute(
        db.select(VitalSign)
        .where(
            VitalSign.encounter_id == encounter.id
        )
        .order_by(
            VitalSign.recorded_at.desc(),
            VitalSign.id.desc(),
        )
    ).scalars().all()

    clinical_notes = db.session.execute(
        db.select(ClinicalNote)
        .where(
            ClinicalNote.encounter_id == encounter.id
        )
        .order_by(
            ClinicalNote.created_at.desc(),
            ClinicalNote.id.desc(),
        )
    ).scalars().all()

    diagnoses = db.session.execute(
        db.select(Diagnosis)
        .where(
            Diagnosis.encounter_id == encounter.id
        )
        .order_by(
            Diagnosis.recorded_at.desc(),
            Diagnosis.id.desc(),
        )
    ).scalars().all()

    investigations = db.session.execute(
        db.select(Investigation)
        .where(
            Investigation.encounter_id == encounter.id
        )
        .order_by(
            Investigation.requested_at.desc(),
            Investigation.id.desc(),
        )
    ).scalars().all()

    return render_template(
        "clinical/encounter_detail.html",
        encounter=encounter,
        patient=encounter.patient,
        chief_complaints=chief_complaints,
        vital_signs=vital_signs,
        clinical_notes=clinical_notes,
        diagnoses=diagnoses,
        investigations=investigations,
    )


@bp.route(
    "/encounters/<int:encounter_id>/chief-complaints/new",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Receptionist",
    "Doctor",
    "Nurse",
)
def add_chief_complaint(encounter_id):
    """Record a structured chief complaint for an encounter."""

    encounter = db.get_or_404(
        Encounter,
        encounter_id,
    )

    if encounter.status != "Open":
        flash(
            "Chief complaints cannot be added to a closed encounter.",
            "warning",
        )

        return redirect(
            url_for(
                "clinical.encounter_detail",
                encounter_id=encounter.id,
            )
        )

    form = ChiefComplaintForm()

    if form.validate_on_submit():
        chief_complaint = ChiefComplaint(
            encounter_id=encounter.id,
            complaint=form.complaint.data.strip(),
            onset=(
                form.onset.data.strip()
                if form.onset.data
                else None
            ),
            duration=(
                form.duration.data.strip()
                if form.duration.data
                else None
            ),
            severity=(
                form.severity.data
                if form.severity.data
                else None
            ),
            recorded_by_id=current_user.id,
        )

        db.session.add(chief_complaint)
        db.session.commit()

        flash(
            "Chief complaint recorded successfully.",
            "success",
        )

        return redirect(
            url_for(
                "clinical.encounter_detail",
                encounter_id=encounter.id,
            )
        )

    return render_template(
        "clinical/add_chief_complaint.html",
        encounter=encounter,
        patient=encounter.patient,
        form=form,
    )


@bp.route(
    "/encounters/<int:encounter_id>/vital-signs/new",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
    "Nurse",
)
def add_vital_signs(encounter_id):
    """Record structured vital signs for an encounter."""

    encounter = db.get_or_404(
        Encounter,
        encounter_id,
    )

    if encounter.status != "Open":
        flash(
            "Vital signs cannot be added to a closed encounter.",
            "warning",
        )

        return redirect(
            url_for(
                "clinical.encounter_detail",
                encounter_id=encounter.id,
            )
        )

    form = VitalSignForm()

    if form.validate_on_submit():
        vital_sign = VitalSign(
            encounter_id=encounter.id,
            temperature_c=form.temperature_c.data,
            heart_rate_bpm=form.heart_rate_bpm.data,
            respiratory_rate_bpm=form.respiratory_rate_bpm.data,
            systolic_bp=form.systolic_bp.data,
            diastolic_bp=form.diastolic_bp.data,
            oxygen_saturation_pct=form.oxygen_saturation_pct.data,
            weight_kg=form.weight_kg.data,
            height_cm=form.height_cm.data,
            recorded_by_id=current_user.id,
        )

        db.session.add(vital_sign)
        db.session.commit()

        flash(
            "Vital signs recorded successfully.",
            "success",
        )

        return redirect(
            url_for(
                "clinical.encounter_detail",
                encounter_id=encounter.id,
            )
        )

    return render_template(
        "clinical/add_vital_signs.html",
        encounter=encounter,
        patient=encounter.patient,
        form=form,
    )


@bp.route(
    "/encounters/<int:encounter_id>/clinical-notes/new",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
    "Nurse",
)
def add_clinical_note(encounter_id):
    """Record a structured clinical note for an encounter."""

    encounter = db.get_or_404(
        Encounter,
        encounter_id,
    )

    if encounter.status != "Open":
        flash(
            "Clinical notes cannot be added to a closed encounter.",
            "warning",
        )

        return redirect(
            url_for(
                "clinical.encounter_detail",
                encounter_id=encounter.id,
            )
        )

    form = ClinicalNoteForm()

    if form.validate_on_submit():
        note = ClinicalNote(
            encounter_id=encounter.id,
            note_type=form.note_type.data,
            subjective=(
                form.subjective.data.strip()
                if form.subjective.data
                else None
            ),
            objective=(
                form.objective.data.strip()
                if form.objective.data
                else None
            ),
            assessment=(
                form.assessment.data.strip()
                if form.assessment.data
                else None
            ),
            plan=(
                form.plan.data.strip()
                if form.plan.data
                else None
            ),
            created_by_id=current_user.id,
        )

        db.session.add(note)
        db.session.commit()

        flash(
            "Clinical note recorded successfully.",
            "success",
        )

        return redirect(
            url_for(
                "clinical.encounter_detail",
                encounter_id=encounter.id,
            )
        )

    return render_template(
        "clinical/add_clinical_note.html",
        encounter=encounter,
        patient=encounter.patient,
        form=form,
    )




@bp.route(
    "/encounters/<int:encounter_id>/diagnoses/new",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
)
def add_diagnosis(encounter_id):
    """Record a clinician-documented encounter diagnosis."""

    encounter = db.get_or_404(
        Encounter,
        encounter_id,
    )

    if encounter.status != "Open":
        flash(
            "Diagnoses cannot be added to a closed encounter.",
            "warning",
        )

        return redirect(
            url_for(
                "clinical.encounter_detail",
                encounter_id=encounter.id,
            )
        )

    form = DiagnosisForm()

    if form.validate_on_submit():
        diagnosis = Diagnosis(
            encounter_id=encounter.id,
            diagnosis_text=form.diagnosis_text.data.strip(),
            diagnosis_type=form.diagnosis_type.data,
            code=(
                form.code.data.strip()
                if form.code.data
                else None
            ),
            code_system=(
                form.code_system.data
                if form.code_system.data
                else None
            ),
            recorded_by_id=current_user.id,
        )

        db.session.add(diagnosis)
        db.session.commit()

        flash(
            "Diagnosis recorded successfully.",
            "success",
        )

        return redirect(
            url_for(
                "clinical.encounter_detail",
                encounter_id=encounter.id,
            )
        )

    return render_template(
        "clinical/add_diagnosis.html",
        encounter=encounter,
        patient=encounter.patient,
        form=form,
    )


@bp.route(
    "/encounters/<int:encounter_id>/investigations/new",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Doctor",
)
def add_investigation(encounter_id):
    """Order a diagnostic investigation for an encounter."""

    encounter = db.get_or_404(
        Encounter,
        encounter_id,
    )

    if encounter.status != "Open":
        flash(
            "Investigations cannot be ordered for a closed encounter.",
            "warning",
        )

        return redirect(
            url_for(
                "clinical.encounter_detail",
                encounter_id=encounter.id,
            )
        )

    form = InvestigationForm()

    if form.validate_on_submit():
        investigation = Investigation(
            encounter_id=encounter.id,
            investigation_name=(
                form.investigation_name.data.strip()
            ),
            category=form.category.data,
            priority=form.priority.data,
            status="Ordered",
            clinical_indication=(
                form.clinical_indication.data.strip()
                if form.clinical_indication.data
                else None
            ),
            requested_by_id=current_user.id,
        )

        db.session.add(investigation)
        db.session.commit()

        flash(
            "Investigation ordered successfully.",
            "success",
        )

        return redirect(
            url_for(
                "clinical.encounter_detail",
                encounter_id=encounter.id,
            )
        )

    return render_template(
        "clinical/add_investigation.html",
        encounter=encounter,
        patient=encounter.patient,
        form=form,
    )
