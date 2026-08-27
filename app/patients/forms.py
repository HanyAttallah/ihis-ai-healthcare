from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    EmailField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional,
    ValidationError,
)


class PatientRegistrationForm(FlaskForm):
    """Form used to register a new patient in iHIS."""

    first_name = StringField(
        "First name",
        validators=[
            DataRequired(),
            Length(min=1, max=80),
        ],
    )

    middle_name = StringField(
        "Middle name",
        validators=[
            Optional(),
            Length(max=80),
        ],
    )

    last_name = StringField(
        "Last name",
        validators=[
            DataRequired(),
            Length(min=1, max=80),
        ],
    )

    date_of_birth = DateField(
        "Date of birth",
        validators=[
            DataRequired(),
        ],
    )

    sex = SelectField(
        "Sex",
        choices=[
            ("", "Select"),
            ("Female", "Female"),
            ("Male", "Male"),
            ("Other", "Other"),
            ("Unknown", "Unknown"),
        ],
        validators=[
            DataRequired(),
        ],
    )

    phone = StringField(
        "Phone",
        validators=[
            Optional(),
            Length(max=30),
        ],
    )

    email = EmailField(
        "Email",
        validators=[
            Optional(),
            Email(),
            Length(max=120),
        ],
    )

    address = TextAreaField(
        "Address",
        validators=[
            Optional(),
            Length(max=255),
        ],
    )

    emergency_contact_name = StringField(
        "Emergency contact name",
        validators=[
            Optional(),
            Length(max=160),
        ],
    )

    emergency_contact_phone = StringField(
        "Emergency contact phone",
        validators=[
            Optional(),
            Length(max=30),
        ],
    )

    submit = SubmitField("Register patient")

    def validate_date_of_birth(self, field):
        """Prevent future dates of birth."""

        if field.data and field.data > date.today():
            raise ValidationError(
                "Date of birth cannot be in the future."
            )
