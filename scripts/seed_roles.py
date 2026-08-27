from app import create_app
from app.extensions import db
from app.models import Role


ROLE_NAMES = [
    "Administrator",
    "Receptionist",
    "Doctor",
    "Nurse",
    "Radiologist",
    "Pharmacist",
]


def seed_roles():
    """Create the standard iHIS roles if they do not already exist."""

    app = create_app()

    with app.app_context():
        created = 0

        for role_name in ROLE_NAMES:
            existing_role = db.session.execute(
                db.select(Role).filter_by(name=role_name)
            ).scalar_one_or_none()

            if existing_role is None:
                db.session.add(Role(name=role_name))
                created += 1

        db.session.commit()

        print(f"Roles created: {created}")
        print(f"Total standard roles: {len(ROLE_NAMES)}")


if __name__ == "__main__":
    seed_roles()
