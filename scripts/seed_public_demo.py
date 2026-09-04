import os
from datetime import date

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import Patient, Role, User


DEMO_PASSWORD_METHOD = "pbkdf2:sha256:600000"


def seed_public_demo():
    """Create an idempotent synthetic public-demo account and patient."""

    app = create_app()

    username = os.getenv("IHIS_DEMO_USERNAME", "demo").strip()
    password = os.getenv("IHIS_DEMO_PASSWORD", "").strip()
    email = os.getenv("IHIS_DEMO_EMAIL", "demo@example.com").strip().lower()

    if not password:
        raise RuntimeError(
            "IHIS_DEMO_PASSWORD must be set before deploying the public demo."
        )

    if len(password) < 12:
        raise RuntimeError(
            "IHIS_DEMO_PASSWORD must contain at least 12 characters."
        )

    with app.app_context():
        administrator_role = db.session.execute(
            db.select(Role).filter_by(name="Administrator")
        ).scalar_one_or_none()

        if administrator_role is None:
            raise RuntimeError(
                "Administrator role is missing. Run scripts.seed_roles first."
            )

        user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

        password_hash = generate_password_hash(
            password,
            method=DEMO_PASSWORD_METHOD,
        )

        if user is None:
            user = User(
                username=username,
                email=email,
                role=administrator_role,
                password_hash=password_hash,
            )
            db.session.add(user)
            db.session.flush()
        else:
            user.email = email
            user.role = administrator_role
            user.is_active_user = True
            user.password_hash = password_hash
            db.session.flush()

        patient = db.session.execute(
            db.select(Patient).filter_by(mrn="IHIS-DEMO-0001")
        ).scalar_one_or_none()

        if patient is None:
            patient = Patient(
                mrn="IHIS-DEMO-0001",
                first_name="Synthetic",
                middle_name="Respiratory",
                last_name="Demo",
                date_of_birth=date(1971, 1, 15),
                sex="Male",
                phone=None,
                email=None,
                address="Synthetic educational record",
                emergency_contact_name=None,
                emergency_contact_phone=None,
                created_by_id=user.id,
            )
            db.session.add(patient)

        db.session.commit()

        print("Public educational demo seeded successfully.")
        print(f"Demo username: {username}")
        print("Synthetic patient MRN: IHIS-DEMO-0001")


if __name__ == "__main__":
    seed_public_demo()
