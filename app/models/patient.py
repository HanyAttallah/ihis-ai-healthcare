from datetime import date, datetime, timezone

from app.extensions import db


class Patient(db.Model):
    """Core demographic record for an iHIS patient."""

    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)

    mrn = db.Column(
        db.String(32),
        unique=True,
        nullable=False,
        index=True,
    )

    first_name = db.Column(
        db.String(80),
        nullable=False,
    )

    middle_name = db.Column(
        db.String(80),
        nullable=True,
    )

    last_name = db.Column(
        db.String(80),
        nullable=False,
    )

    date_of_birth = db.Column(
        db.Date,
        nullable=False,
    )

    sex = db.Column(
        db.String(20),
        nullable=False,
    )

    phone = db.Column(
        db.String(30),
        nullable=True,
    )

    email = db.Column(
        db.String(120),
        nullable=True,
    )

    address = db.Column(
        db.String(255),
        nullable=True,
    )

    emergency_contact_name = db.Column(
        db.String(160),
        nullable=True,
    )

    emergency_contact_phone = db.Column(
        db.String(30),
        nullable=True,
    )

    is_active = db.Column(
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

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    created_by = db.relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    encounters = db.relationship(
        "Encounter",
        back_populates="patient",
        cascade="all, delete-orphan",
        lazy="select",
    )

    @property
    def full_name(self):
        """Return the patient's formatted full name."""

        names = [
            self.first_name,
            self.middle_name,
            self.last_name,
        ]

        return " ".join(
            name.strip()
            for name in names
            if name and name.strip()
        )

    @property
    def age(self):
        """Calculate age dynamically from date of birth."""

        if self.date_of_birth is None:
            return None

        today = date.today()

        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (
                    self.date_of_birth.month,
                    self.date_of_birth.day,
                )
            )
        )

    def __repr__(self):
        return f"<Patient {self.mrn}: {self.full_name}>"

