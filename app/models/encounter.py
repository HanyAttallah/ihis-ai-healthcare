from datetime import datetime, timezone

from app.extensions import db


class Encounter(db.Model):
    """A clinical encounter linked to one iHIS patient."""

    __tablename__ = "encounters"

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

    encounter_type = db.Column(
        db.String(50),
        nullable=False,
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Open",
    )

    department = db.Column(
        db.String(100),
        nullable=True,
    )

    presenting_complaint = db.Column(
        db.String(500),
        nullable=True,
    )

    created_by_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    started_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    closed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    patient = db.relationship(
        "Patient",
        back_populates="encounters",
    )

    created_by = db.relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    chief_complaints = db.relationship(
        "ChiefComplaint",
        back_populates="encounter",
        cascade="all, delete-orphan",
        lazy="select",
    )

    vital_signs = db.relationship(
        "VitalSign",
        back_populates="encounter",
        cascade="all, delete-orphan",
        lazy="select",
    )

    clinical_notes = db.relationship(
        "ClinicalNote",
        back_populates="encounter",
        cascade="all, delete-orphan",
        lazy="select",
    )

    diagnoses = db.relationship(
        "Diagnosis",
        back_populates="encounter",
        cascade="all, delete-orphan",
        lazy="select",
    )

    investigations = db.relationship(
        "Investigation",
        back_populates="encounter",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self):
        return (
            f"<Encounter {self.id}: "
            f"{self.patient_id} / {self.encounter_type}>"
        )
