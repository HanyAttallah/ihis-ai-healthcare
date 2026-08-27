from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DecimalField,
    IntegerField,
    SubmitField,
)
from wtforms.validators import DataRequired, NumberRange


class GPConsultationForm(FlaskForm):
    age = IntegerField(
        "Age",
        validators=[
            DataRequired(),
            NumberRange(min=18, max=100),
        ],
    )

    temperature = DecimalField(
        "Temperature (?C)",
        places=1,
        validators=[
            DataRequired(),
            NumberRange(min=34, max=43),
        ],
    )

    heart_rate = IntegerField(
        "Heart rate (beats/min)",
        validators=[
            DataRequired(),
            NumberRange(min=30, max=220),
        ],
    )

    cough = BooleanField("Cough")
    sputum = BooleanField("Sputum production")
    dyspnea = BooleanField("Shortness of breath")
    dysuria = BooleanField("Painful urination")
    urinary_frequency = BooleanField("Urinary frequency")
    abdominal_pain = BooleanField("Abdominal pain")
    diarrhea = BooleanField("Diarrhea")
    vomiting = BooleanField("Vomiting")
    smoking = BooleanField("Smoking")

    submit = SubmitField("Run GP AI Prediction")
