from datetime import datetime, timezone

from app.extensions import db


class ChiefComplaint(db.Model):
    """A presenting complaint documented during a clinical encounter."""

    __tablename__ = "chief_complaints"

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

    complaint = db.Column(
        db.String(500),
        nullable=False,
    )

    onset = db.Column(
        db.String(120),
        nullable=True,
    )

    duration = db.Column(
        db.String(120),
        nullable=True,
    )

    severity = db.Column(
        db.String(30),
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
        back_populates="chief_complaints",
    )

    recorded_by = db.relationship(
        "User",
        foreign_keys=[recorded_by_id],
    )

    def __repr__(self):
        return (
            f"<ChiefComplaint {self.id}: "
            f"encounter={self.encounter_id}>"
        )
