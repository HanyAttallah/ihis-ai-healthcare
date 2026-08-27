from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import Length, Optional


class MedicationSafetyForm(FlaskForm):
    condition = SelectField(
        "Clinical context",
        choices=[
            ("Fever or mild pain", "Fever or mild pain"),
            ("Type 2 diabetes", "Type 2 diabetes"),
            (
                "Suspected bacterial respiratory infection",
                "Suspected bacterial respiratory infection",
            ),
            (
                "Urinary tract infection",
                "Urinary tract infection",
            ),
        ],
    )

    current_medications = StringField(
        "Current medications",
        validators=[
            Optional(),
            Length(max=500),
        ],
        description=(
            "Enter comma-separated generic names, "
            "for example: warfarin, ibuprofen"
        ),
    )

    allergies = StringField(
        "Known medication allergies",
        validators=[
            Optional(),
            Length(max=300),
        ],
    )

    renal_impairment = BooleanField(
        "Known renal impairment"
    )

    submit = SubmitField(
        "Run Medication Safety Check"
    )
