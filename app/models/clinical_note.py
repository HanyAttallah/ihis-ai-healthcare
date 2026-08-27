from datetime import datetime, timezone

from app.extensions import db


class ClinicalNote(db.Model):
    """A structured clinical note documented during an encounter."""

    __tablename__ = "clinical_notes"

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

    note_type = db.Column(
        db.String(50),
        nullable=False,
    )

    subjective = db.Column(
        db.Text,
        nullable=True,
    )

    objective = db.Column(
        db.Text,
        nullable=True,
    )

    assessment = db.Column(
        db.Text,
        nullable=True,
    )

    plan = db.Column(
        db.Text,
        nullable=True,
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

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    encounter = db.relationship(
        "Encounter",
        back_populates="clinical_notes",
    )

    created_by = db.relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    def __repr__(self):
        return (
            f"<ClinicalNote {self.id}: "
            f"encounter={self.encounter_id}, "
            f"type={self.note_type}>"
        )
