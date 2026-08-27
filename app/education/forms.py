from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PatientQuestionForm(FlaskForm):
    question = TextAreaField(
        "Ask a health question",
        validators=[
            DataRequired(),
            Length(min=3, max=1000),
        ],
    )

    submit = SubmitField(
        "Ask Patient Education AI"
    )
