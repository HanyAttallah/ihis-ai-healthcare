from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ICUMonitorForm(FlaskForm):
    temperature = DecimalField(
        "Temperature (?C)",
        places=1,
        validators=[
            DataRequired(),
            NumberRange(min=30, max=45),
        ],
    )

    heart_rate = IntegerField(
        "Heart rate (beats/min)",
        validators=[
            DataRequired(),
            NumberRange(min=20, max=250),
        ],
    )

    respiratory_rate = IntegerField(
        "Respiratory rate (/min)",
        validators=[
            DataRequired(),
            NumberRange(min=4, max=80),
        ],
    )

    systolic_bp = IntegerField(
        "Systolic BP (mmHg)",
        validators=[
            DataRequired(),
            NumberRange(min=40, max=300),
        ],
    )

    oxygen_saturation = DecimalField(
        "SpO2 (%)",
        places=1,
        validators=[
            DataRequired(),
            NumberRange(min=30, max=100),
        ],
    )

    submit = SubmitField("Analyze ICU Vitals")
