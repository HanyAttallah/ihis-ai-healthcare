from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Secure login form for iHIS users."""

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=80),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=1, max=128),
        ],
    )

    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")


class LogoutForm(FlaskForm):
    """CSRF-protected logout form."""

    submit = SubmitField("Sign out")
