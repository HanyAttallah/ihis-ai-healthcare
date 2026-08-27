from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from app.auth.decorators import roles_required
from app.extensions import db
from app.models import AIAssessment, AIReview, Patient
from app.receptionist import bp
from app.receptionist.forms import AIReviewForm, ReceptionistIntakeForm
from app.services.ai.receptionist import route_patient


@bp.route(
    "/patients/<int:patient_id>/intake",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Receptionist",
)
def intake(patient_id):
    """
    Run explainable receptionist routing support for a registered patient.
    """

    patient = db.get_or_404(
        Patient,
        patient_id,
    )

    form = ReceptionistIntakeForm()

    if form.validate_on_submit():
        symptom_text = form.symptom_text.data.strip()

        additional_context = (
            form.additional_context.data.strip()
            if form.additional_context.data
            else None
        )

        analysis_text = symptom_text

        if additional_context:
            analysis_text = (
                f"{symptom_text}. "
                f"{additional_context}"
            )

        result = route_patient(
            symptom_text=analysis_text,
            symptom_duration=(
                form.symptom_duration.data.strip()
                if form.symptom_duration.data
                else None
            ),
        )

        assessment = AIAssessment(
            patient_id=patient.id,
            encounter_id=None,
            module="Receptionist AI",
            assessment_type="Administrative Intake Routing",
            input_data={
                "symptom_text": symptom_text,
                "symptom_duration": (
                    form.symptom_duration.data.strip()
                    if form.symptom_duration.data
                    else None
                ),
                "additional_context": additional_context,
            },
            output_data={
                "recommended_service": result[
                    "recommended_service"
                ],
                "urgency": result["urgency"],
                "red_flags": result["red_flags"],
                "department_scores": result[
                    "department_scores"
                ],
                "routing_evidence": result[
                    "routing_evidence"
                ],
                "basic_guidance": result[
                    "basic_guidance"
                ],
                "appointment_information": result[
                    "appointment_information"
                ],
                "disclaimer": result["disclaimer"],
            },
            explanation=result["explanation"],
            risk_level=result["urgency"],
            model_name=result["model_name"],
            model_version=result["model_version"],
            human_review_required=True,
            created_by_id=current_user.id,
        )

        db.session.add(assessment)
        db.session.commit()

        flash(
            "Receptionist AI assessment generated. "
            "Human review is required before operational use.",
            "success",
        )

        return redirect(
            url_for(
                "receptionist.assessment_detail",
                assessment_id=assessment.id,
            )
        )

    return render_template(
        "receptionist/intake.html",
        patient=patient,
        form=form,
    )


@bp.route(
    "/assessments/<int:assessment_id>"
)
@roles_required(
    "Administrator",
    "Receptionist",
    "Doctor",
    "Nurse",
)
def assessment_detail(assessment_id):
    """Display one receptionist AI assessment and its review status."""

    assessment = db.get_or_404(
        AIAssessment,
        assessment_id,
    )

    review = db.session.execute(
        db.select(AIReview)
        .where(
            AIReview.assessment_id == assessment.id
        )
        .order_by(
            AIReview.reviewed_at.desc(),
            AIReview.id.desc(),
        )
    ).scalars().first()

    return render_template(
        "receptionist/assessment_detail.html",
        assessment=assessment,
        patient=assessment.patient,
        review=review,
    )




@bp.route(
    "/assessments/<int:assessment_id>/review",
    methods=["GET", "POST"],
)
@roles_required(
    "Administrator",
    "Receptionist",
    "Doctor",
    "Nurse",
)
def review_assessment(assessment_id):
    """Record human review of a receptionist AI assessment."""

    assessment = db.get_or_404(
        AIAssessment,
        assessment_id,
    )

    existing_review = db.session.execute(
        db.select(AIReview)
        .where(
            AIReview.assessment_id == assessment.id
        )
        .order_by(
            AIReview.reviewed_at.desc(),
            AIReview.id.desc(),
        )
    ).scalars().first()

    if existing_review:
        flash(
            "This AI assessment has already been reviewed.",
            "info",
        )

        return redirect(
            url_for(
                "receptionist.assessment_detail",
                assessment_id=assessment.id,
            )
        )

    form = AIReviewForm()

    if form.validate_on_submit():
        decision = form.decision.data

        modified_output = None

        if decision == "Modified":
            modified_output = {
                "recommended_service": (
                    form.final_service.data
                ),
                "urgency": (
                    form.final_urgency.data
                ),
                "original_recommended_service": (
                    assessment.output_data[
                        "recommended_service"
                    ]
                ),
                "original_urgency": (
                    assessment.output_data[
                        "urgency"
                    ]
                ),
            }

        review = AIReview(
            assessment_id=assessment.id,
            decision=decision,
            comments=(
                form.comments.data.strip()
                if form.comments.data
                else None
            ),
            modified_output=modified_output,
            reviewer_id=current_user.id,
        )

        db.session.add(review)
        db.session.commit()

        flash(
            "Human review recorded successfully.",
            "success",
        )

        return redirect(
            url_for(
                "receptionist.assessment_detail",
                assessment_id=assessment.id,
            )
        )

    return render_template(
        "receptionist/review.html",
        assessment=assessment,
        patient=assessment.patient,
        form=form,
    )

