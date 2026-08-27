from getpass import getpass

from app import create_app
from app.extensions import db
from app.models import Role, User


def create_administrator():
    """Interactively create the first iHIS Administrator account."""

    app = create_app()

    with app.app_context():
        administrator_role = db.session.execute(
            db.select(Role).filter_by(name="Administrator")
        ).scalar_one_or_none()

        if administrator_role is None:
            print("ERROR: Administrator role does not exist.")
            print("Run the role-seeding script first.")
            return

        username = input("Administrator username: ").strip()
        email = input("Administrator email: ").strip().lower()

        if not username or not email:
            print("ERROR: Username and email are required.")
            return

        existing_username = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

        if existing_username is not None:
            print("ERROR: Username already exists.")
            return

        existing_email = db.session.execute(
            db.select(User).filter_by(email=email)
        ).scalar_one_or_none()

        if existing_email is not None:
            print("ERROR: Email already exists.")
            return

        password = getpass("Administrator password: ")
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            print("ERROR: Passwords do not match.")
            return

        if len(password) < 12:
            print("ERROR: Password must contain at least 12 characters.")
            return

        administrator = User(
            username=username,
            email=email,
            role=administrator_role,
        )

        administrator.set_password(password)

        db.session.add(administrator)
        db.session.commit()

        print("Administrator account created successfully.")
        print(f"Username: {administrator.username}")
        print(f"Role: {administrator.role.name}")


if __name__ == "__main__":
    create_administrator()
