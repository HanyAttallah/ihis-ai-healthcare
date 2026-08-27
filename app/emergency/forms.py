from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField


class EmergencyBFSForm(FlaskForm):
    chest_pain = BooleanField("Chest pain")
    dyspnea = BooleanField("Shortness of breath")
    sweating = BooleanField("Sweating")
    nausea = BooleanField("Nausea")
    tachycardia = BooleanField("Tachycardia")
    hemoptysis = BooleanField("Hemoptysis")
    wheeze = BooleanField("Wheeze")
    chest_tightness = BooleanField("Chest tightness")

    sudden_weakness = BooleanField("Sudden weakness")
    speech_difficulty = BooleanField("Speech difficulty")
    seizure = BooleanField("Seizure")
    altered_consciousness = BooleanField("Altered consciousness")

    fever = BooleanField("Fever")
    hypotension = BooleanField("Hypotension")
    rash = BooleanField("Rash")
    swelling = BooleanField("Facial / airway swelling")

    submit = SubmitField(
        "Run BFS Emergency Assessment"
    )
