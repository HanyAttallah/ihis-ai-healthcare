from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    SelectField,
    SubmitField,
)
from wtforms.validators import DataRequired


class OncologyDFSForm(FlaskForm):
    persistent_cough = BooleanField("Persistent cough")
    hemoptysis = BooleanField("Hemoptysis")
    dyspnea = BooleanField("Shortness of breath")
    chest_pain = BooleanField("Chest pain")
    weight_loss = BooleanField("Unintentional weight loss")
    smoking_history = BooleanField("Smoking history")

    rectal_bleeding = BooleanField("Rectal bleeding")
    change_bowel_habit = BooleanField("Change in bowel habit")
    abdominal_pain = BooleanField("Abdominal pain")
    anemia = BooleanField("Anemia")

    urinary_obstruction = BooleanField(
        "Urinary obstructive symptoms"
    )
    hematuria = BooleanField("Hematuria")
    bone_pain = BooleanField("Bone pain")
    elevated_psa = BooleanField("Elevated PSA")

    submit = SubmitField("Run Oncology DFS")


class TreatmentRLForm(FlaskForm):
    disease_extent = SelectField(
        "Simulated disease extent",
        choices=[
            ("", "Select extent"),
            ("Localized", "Localized"),
            ("Locally advanced", "Locally advanced"),
            ("Metastatic", "Metastatic"),
        ],
        validators=[DataRequired()],
    )

    ecog_status = SelectField(
        "ECOG Performance Status",
        choices=[
            ("", "Select ECOG status"),
            ("0", "ECOG 0 — Fully active"),
            (
                "1",
                "ECOG 1 — Restricted strenuous activity; ambulatory",
            ),
            (
                "2",
                "ECOG 2 — Ambulatory/self-care; unable to work",
            ),
            (
                "3",
                "ECOG 3 — Limited self-care; bed/chair >50% of waking hours",
            ),
            (
                "4",
                "ECOG 4 — Completely disabled",
            ),
        ],
        validators=[DataRequired()],
    )

    submit = SubmitField(
        "Run RL Treatment Simulation"
    )
