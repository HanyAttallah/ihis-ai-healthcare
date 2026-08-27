from datetime import datetime, timezone

from app.extensions import db


class Investigation(db.Model):
    """A diagnostic investigation requested during an encounter."""

    __tablename__ = "investigations"

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

    investigation_name = db.Column(
        db.String(200),
        nullable=False,
    )

    category = db.Column(
        db.String(50),
        nullable=False,
    )

    priority = db.Column(
        db.String(30),
        nullable=False,
        default="Routine",
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Ordered",
    )

    clinical_indication = db.Column(
        db.String(1000),
        nullable=True,
    )

    requested_by_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    requested_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    encounter = db.relationship(
        "Encounter",
        back_populates="investigations",
    )

    requested_by = db.relationship(
        "User",
        foreign_keys=[requested_by_id],
    )

    def __repr__(self):
        return (
            f"<Investigation {self.id}: "
            f"encounter={self.encounter_id}, "
            f"name={self.investigation_name}>"
        )
