from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class Role(db.Model):
    """Application role used for role-based access control."""

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    users = db.relationship(
        "User",
        back_populates="role",
        lazy="select"
    )

    def __repr__(self):
        return f"<Role {self.name}>"


class User(UserMixin, db.Model):
    """Authenticated iHIS user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
        index=True
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(256),
        nullable=False
    )

    is_active_user = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id"),
        nullable=False
    )

    role = db.relationship(
        "Role",
        back_populates="users"
    )

    def set_password(self, password):
        """Store a secure password hash rather than plaintext."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Validate a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.is_active_user

    def has_role(self, role_name):
        """Return True if the user has the requested role."""
        return self.role is not None and self.role.name == role_name

    def __repr__(self):
        return f"<User {self.username}>"


@login_manager.user_loader
def load_user(user_id):
    """Load an authenticated user for Flask-Login."""
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None
