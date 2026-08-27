from datetime import datetime, timezone

from app.extensions import db


class Diagnosis(db.Model):
    """A clinician-documented diagnosis linked to an encounter."""

    __tablename__ = "diagnoses"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    encounter_id = db.Column(
        db.Integer,
        db.ForeignKey("encounters.id"),
        nullable=False,
        index=True,
    )

    diagnosis_text = db.Column(
        db.String(500),
        nullable=False,
    )

    diagnosis_type = db.Column(
        db.String(50),
        nullable=False,
        default="Working",
    )

    code = db.Column(
        db.String(50),
        nullable=True,
    )

    code_system = db.Column(
        db.String(50),
        nullable=True,
    )

    recorded_by_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    recorded_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    encounter = db.relationship(
        "Encounter",
        back_populates="diagnoses",
    )

    recorded_by = db.relationship(
        "User",
        foreign_keys=[recorded_by_id],
    )

    def __repr__(self):
        return (
            f"<Diagnosis {self.id}: "
            f"encounter={self.encounter_id}, "
            f"type={self.diagnosis_type}>"
        )
