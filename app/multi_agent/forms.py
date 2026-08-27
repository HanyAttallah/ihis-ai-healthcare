from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class MultiAgentDemoForm(FlaskForm):
    scenario = SelectField(
        "Synthetic demonstration scenario",
        choices=[
            (
                "respiratory",
                "Respiratory case - GP / Imaging / Reasoning",
            ),
            (
                "emergency",
                "Emergency neurological case - ICU / Emergency",
            ),
            (
                "mental_health",
                "Mental-health case - Psychiatrist",
            ),
            (
                "oncology",
                "Oncology case - DFS / Treatment Planning",
            ),
        ],
        validators=[DataRequired()],
    )

    submit = SubmitField(
        "Run Relevance-Selected Multi-Agent Case"
    )
