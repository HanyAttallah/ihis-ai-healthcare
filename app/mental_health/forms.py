from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired


SCREENING_CHOICES = [
    (0, "0 — Not at all"),
    (1, "1 — Several days"),
    (2, "2 — More than half the days"),
    (3, "3 — Nearly every day"),
]


class MentalHealthAssessmentForm(FlaskForm):
    low_interest = SelectField(
        "Little interest or pleasure in doing things",
        choices=SCREENING_CHOICES,
        coerce=int,
        validators=[InputRequired()],
    )

    depressed_mood = SelectField(
        "Feeling down, depressed, or hopeless",
        choices=SCREENING_CHOICES,
        coerce=int,
        validators=[InputRequired()],
    )

    nervous = SelectField(
        "Feeling nervous, anxious, or on edge",
        choices=SCREENING_CHOICES,
        coerce=int,
        validators=[InputRequired()],
    )

    unable_to_stop_worrying = SelectField(
        "Not being able to stop or control worrying",
        choices=SCREENING_CHOICES,
        coerce=int,
        validators=[InputRequired()],
    )

    submit = SubmitField("Run Psychiatrist AI Screening")
