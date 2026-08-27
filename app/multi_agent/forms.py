from flask_wtf import FlaskForm
from wtforms import SubmitField


class MultiAgentDemoForm(FlaskForm):
    submit = SubmitField(
        "Run Integrated Multi-Agent Case"
    )
