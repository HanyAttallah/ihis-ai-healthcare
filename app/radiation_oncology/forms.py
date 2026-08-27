from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    IntegerField,
    SelectField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    NumberRange,
)


MUCOSITIS_CHOICES = [
    ("0", "Grade 0 — None"),
    (
        "1",
        "Grade 1 — Asymptomatic/mild; no intervention indicated",
    ),
    (
        "2",
        "Grade 2 — Moderate pain/ulcer; oral intake maintained with modified diet",
    ),
    (
        "3",
        "Grade 3 — Severe pain interfering with oral intake",
    ),
    (
        "4",
        "Grade 4 — Life-threatening; urgent intervention indicated",
    ),
]


DERMATITIS_CHOICES = [
    ("0", "Grade 0 — None"),
    (
        "1",
        "Grade 1 — Faint erythema or dry desquamation",
    ),
    (
        "2",
        "Grade 2 — Brisk erythema / patchy moist desquamation in folds",
    ),
    (
        "3",
        "Grade 3 — Moist desquamation outside folds / trauma-induced bleeding",
    ),
    (
        "4",
        "Grade 4 — Necrosis/full-thickness ulceration/spontaneous bleeding",
    ),
]


DYSPHAGIA_CHOICES = [
    ("0", "Grade 0 — None"),
    (
        "1",
        "Grade 1 — Symptomatic; able to eat regular diet",
    ),
    (
        "2",
        "Grade 2 — Altered eating/swallowing",
    ),
    (
        "3",
        "Grade 3 — Severely altered swallowing; tube feeding/TPN/hospitalization indicated",
    ),
    (
        "4",
        "Grade 4 — Life-threatening; urgent intervention indicated",
    ),
]


NAUSEA_CHOICES = [
    ("0", "Grade 0 — None"),
    (
        "1",
        "Grade 1 — Appetite loss without altered eating habits",
    ),
    (
        "2",
        "Grade 2 — Decreased oral intake without significant weight loss/dehydration/malnutrition",
    ),
    (
        "3",
        "Grade 3 — Inadequate oral intake; tube feeding/TPN/hospitalization indicated",
    ),
]


VOMITING_CHOICES = [
    ("0", "Grade 0 — None"),
    (
        "1",
        "Grade 1 — Intervention not indicated",
    ),
    (
        "2",
        "Grade 2 — Outpatient IV hydration / medical intervention indicated",
    ),
    (
        "3",
        "Grade 3 — Tube feeding/TPN/hospitalization indicated",
    ),
    (
        "4",
        "Grade 4 — Life-threatening consequences",
    ),
]


FATIGUE_CHOICES = [
    ("0", "Grade 0 — None"),
    (
        "1",
        "Grade 1 — Relieved by rest",
    ),
    (
        "2",
        "Grade 2 — Not relieved by rest; limiting instrumental ADL",
    ),
    (
        "3",
        "Grade 3 — Not relieved by rest; limiting self-care ADL",
    ),
]


class RadiationToxicityForm(FlaskForm):

    mucositis_oral = SelectField(
        "Oral mucositis — CTCAE v5.0",
        choices=MUCOSITIS_CHOICES,
        validators=[DataRequired()],
    )

    dermatitis_radiation = SelectField(
        "Radiation dermatitis — CTCAE v5.0",
        choices=DERMATITIS_CHOICES,
        validators=[DataRequired()],
    )

    dysphagia = SelectField(
        "Dysphagia — CTCAE v5.0",
        choices=DYSPHAGIA_CHOICES,
        validators=[DataRequired()],
    )

    nausea = SelectField(
        "Nausea — CTCAE v5.0",
        choices=NAUSEA_CHOICES,
        validators=[DataRequired()],
    )

    vomiting = SelectField(
        "Vomiting — CTCAE v5.0",
        choices=VOMITING_CHOICES,
        validators=[DataRequired()],
    )

    fatigue = SelectField(
        "Fatigue — CTCAE v5.0",
        choices=FATIGUE_CHOICES,
        validators=[DataRequired()],
    )

    pain_score = IntegerField(
        "Pain score (0–10)",
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
                max=10,
                message="Pain score must be between 0 and 10.",
            ),
        ],
    )

    weight_loss = BooleanField(
        "Clinically relevant weight loss"
    )

    fever = BooleanField(
        "Fever during treatment"
    )

    submit = SubmitField(
        "Analyze RT Toxicity"
    )
