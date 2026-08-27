from datetime import datetime, timezone

from app.extensions import db


class AIAssessment(db.Model):
    """A traceable AI or algorithmic assessment linked to patient care."""

    __tablename__ = "ai_assessments"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False,
        index=True,
    )

    encounter_id = db.Column(
        db.Integer,
        db.ForeignKey("encounters.id"),
        nullable=True,
        index=True,
    )

    module = db.Column(
        db.String(80),
        nullable=False,
        index=True,
    )

    assessment_type = db.Column(
        db.String(80),
        nullable=False,
    )

    input_data = db.Column(
        db.JSON,
        nullable=False,
    )

    output_data = db.Column(
        db.JSON,
        nullable=False,
    )

    explanation = db.Column(
        db.Text,
        nullable=True,
    )

    risk_level = db.Column(
        db.String(30),
        nullable=True,
    )

    model_name = db.Column(
        db.String(120),
        nullable=False,
    )

    model_version = db.Column(
        db.String(50),
        nullable=True,
    )

    human_review_required = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )

    created_by_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    patient = db.relationship(
        "Patient",
    )

    encounter = db.relationship(
        "Encounter",
    )

    created_by = db.relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    reviews = db.relationship(
        "AIReview",
        back_populates="assessment",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self):
        return (
            f"<AIAssessment {self.id}: "
            f"module={self.module}, "
            f"patient={self.patient_id}>"
        )
