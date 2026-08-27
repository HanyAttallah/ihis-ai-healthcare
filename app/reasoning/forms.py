from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField


class ClinicalReasoningForm(FlaskForm):
    fever = BooleanField("Fever")
    cough = BooleanField("Cough")
    sputum = BooleanField("Sputum production")
    dyspnea = BooleanField("Shortness of breath")
    chest_pain = BooleanField("Chest pain")
    sore_throat = BooleanField("Sore throat")
    nasal_symptoms = BooleanField("Nasal symptoms")
    fatigue = BooleanField("Fatigue")

    dysuria = BooleanField("Painful urination")
    urinary_frequency = BooleanField("Urinary frequency")
    lower_abdominal_pain = BooleanField("Lower abdominal pain")

    abdominal_pain = BooleanField("Abdominal pain")
    diarrhea = BooleanField("Diarrhea")
    vomiting = BooleanField("Vomiting")
    nausea = BooleanField("Nausea")

    sweating = BooleanField("Sweating")
    wheeze = BooleanField("Wheeze")
    chest_tightness = BooleanField("Chest tightness")

    submit = SubmitField(
        "Generate Differential Diagnoses"
    )
