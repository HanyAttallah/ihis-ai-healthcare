from datetime import datetime, timezone

from app.extensions import db


class VitalSign(db.Model):
    """A set of vital-sign observations recorded during an encounter."""

    __tablename__ = "vital_signs"

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

    temperature_c = db.Column(
        db.Float,
        nullable=True,
    )

    heart_rate_bpm = db.Column(
        db.Integer,
        nullable=True,
    )

    respiratory_rate_bpm = db.Column(
        db.Integer,
        nullable=True,
    )

    systolic_bp = db.Column(
        db.Integer,
        nullable=True,
    )

    diastolic_bp = db.Column(
        db.Integer,
        nullable=True,
    )

    oxygen_saturation_pct = db.Column(
        db.Float,
        nullable=True,
    )

    weight_kg = db.Column(
        db.Float,
        nullable=True,
    )

    height_cm = db.Column(
        db.Float,
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
        back_populates="vital_signs",
    )

    recorded_by = db.relationship(
        "User",
        foreign_keys=[recorded_by_id],
    )

    @property
    def bmi(self):
        """Calculate BMI dynamically when height and weight are available."""

        if (
            self.weight_kg is None
            or self.height_cm is None
            or self.height_cm <= 0
        ):
            return None

        height_m = self.height_cm / 100

        return round(
            self.weight_kg / (height_m ** 2),
            1,
        )

    def __repr__(self):
        return (
            f"<VitalSign {self.id}: "
            f"encounter={self.encounter_id}>"
        )
