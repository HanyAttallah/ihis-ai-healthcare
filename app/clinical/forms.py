from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    Optional,
)


class EncounterForm(FlaskForm):
    """Form used to start a new clinical encounter."""

    encounter_type = SelectField(
        "Encounter type",
        choices=[
            ("", "Select encounter type"),
            ("Outpatient", "Outpatient"),
            ("Emergency", "Emergency"),
            ("Inpatient", "Inpatient"),
            ("Follow-up", "Follow-up"),
            ("Telemedicine", "Telemedicine"),
        ],
        validators=[DataRequired()],
    )

    department = StringField(
        "Department / Service",
        validators=[
            Optional(),
            Length(max=100),
        ],
    )

    presenting_complaint = TextAreaField(
        "Presenting complaint / reason for encounter",
        validators=[
            Optional(),
            Length(max=500),
        ],
    )

    submit = SubmitField("Start Encounter")


class ChiefComplaintForm(FlaskForm):
    """Form used to record a structured chief complaint."""

    complaint = TextAreaField(
        "Chief complaint",
        validators=[
            DataRequired(),
            Length(max=500),
        ],
    )

    onset = StringField(
        "Onset",
        validators=[
            Optional(),
            Length(max=120),
        ],
    )

    duration = StringField(
        "Duration",
        validators=[
            Optional(),
            Length(max=120),
        ],
    )

    severity = SelectField(
        "Severity",
        choices=[
            ("", "Not specified"),
            ("Mild", "Mild"),
            ("Moderate", "Moderate"),
            ("Severe", "Severe"),
            ("Unknown", "Unknown"),
        ],
        validators=[Optional()],
    )

    submit = SubmitField("Record Chief Complaint")


class VitalSignForm(FlaskForm):
    """Form used to record structured vital-sign observations."""

    temperature_c = FloatField(
        "Temperature (°C)",
        validators=[
            Optional(),
            NumberRange(
                min=25,
                max=45,
                message="Enter a temperature between 25 and 45 °C.",
            ),
        ],
    )

    heart_rate_bpm = IntegerField(
        "Heart rate (beats/min)",
        validators=[
            Optional(),
            NumberRange(
                min=20,
                max=300,
                message="Enter a heart rate between 20 and 300 beats/min.",
            ),
        ],
    )

    respiratory_rate_bpm = IntegerField(
        "Respiratory rate (breaths/min)",
        validators=[
            Optional(),
            NumberRange(
                min=5,
                max=100,
                message="Enter a respiratory rate between 5 and 100 breaths/min.",
            ),
        ],
    )

    systolic_bp = IntegerField(
        "Systolic BP (mmHg)",
        validators=[
            Optional(),
            NumberRange(
                min=40,
                max=300,
                message="Enter systolic BP between 40 and 300 mmHg.",
            ),
        ],
    )

    diastolic_bp = IntegerField(
        "Diastolic BP (mmHg)",
        validators=[
            Optional(),
            NumberRange(
                min=20,
                max=200,
                message="Enter diastolic BP between 20 and 200 mmHg.",
            ),
        ],
    )

    oxygen_saturation_pct = FloatField(
        "Oxygen saturation (%)",
        validators=[
            Optional(),
            NumberRange(
                min=30,
                max=100,
                message="Enter oxygen saturation between 30 and 100%.",
            ),
        ],
    )

    weight_kg = FloatField(
        "Weight (kg)",
        validators=[
            Optional(),
            NumberRange(
                min=0.5,
                max=500,
                message="Enter weight between 0.5 and 500 kg.",
            ),
        ],
    )

    height_cm = FloatField(
        "Height (cm)",
        validators=[
            Optional(),
            NumberRange(
                min=30,
                max=250,
                message="Enter height between 30 and 250 cm.",
            ),
        ],
    )

    submit = SubmitField("Record Vital Signs")

    def validate(self, extra_validators=None):
        """Apply field validation plus cross-field sanity checks."""

        valid = super().validate(
            extra_validators=extra_validators
        )

        values = [
            self.temperature_c.data,
            self.heart_rate_bpm.data,
            self.respiratory_rate_bpm.data,
            self.systolic_bp.data,
            self.diastolic_bp.data,
            self.oxygen_saturation_pct.data,
            self.weight_kg.data,
            self.height_cm.data,
        ]

        if all(value is None for value in values):
            self.temperature_c.errors.append(
                "Record at least one vital-sign measurement."
            )
            valid = False

        if (
            self.systolic_bp.data is not None
            and self.diastolic_bp.data is not None
            and self.systolic_bp.data <= self.diastolic_bp.data
        ):
            self.systolic_bp.errors.append(
                "Systolic BP must be greater than diastolic BP."
            )
            valid = False

        return valid


class ClinicalNoteForm(FlaskForm):
    """Form used to document a structured clinical note."""

    note_type = SelectField(
        "Note type",
        choices=[
            ("", "Select note type"),
            ("SOAP", "SOAP Note"),
            ("Progress", "Progress Note"),
            ("Consultation", "Consultation Note"),
            ("Nursing", "Nursing Note"),
        ],
        validators=[DataRequired()],
    )

    subjective = TextAreaField(
        "Subjective",
        validators=[
            Optional(),
            Length(max=5000),
        ],
    )

    objective = TextAreaField(
        "Objective",
        validators=[
            Optional(),
            Length(max=5000),
        ],
    )

    assessment = TextAreaField(
        "Assessment",
        validators=[
            Optional(),
            Length(max=5000),
        ],
    )

    plan = TextAreaField(
        "Plan",
        validators=[
            Optional(),
            Length(max=5000),
        ],
    )

    submit = SubmitField("Record Clinical Note")

    def validate(self, extra_validators=None):
        """Require at least one populated clinical-note section."""

        valid = super().validate(
            extra_validators=extra_validators
        )

        sections = [
            self.subjective.data,
            self.objective.data,
            self.assessment.data,
            self.plan.data,
        ]

        has_content = any(
            value is not None and value.strip()
            for value in sections
        )

        if not has_content:
            self.subjective.errors.append(
                "Record at least one clinical-note section."
            )
            valid = False

        return valid


class DiagnosisForm(FlaskForm):
    """Form used to document an encounter diagnosis."""

    diagnosis_text = StringField(
        "Diagnosis",
        validators=[
            DataRequired(),
            Length(max=500),
        ],
    )

    diagnosis_type = SelectField(
        "Diagnosis type",
        choices=[
            ("Working", "Working diagnosis"),
            ("Differential", "Differential diagnosis"),
            ("Confirmed", "Confirmed diagnosis"),
        ],
        validators=[DataRequired()],
    )

    code = StringField(
        "Clinical code",
        validators=[
            Optional(),
            Length(max=50),
        ],
    )

    code_system = SelectField(
        "Code system",
        choices=[
            ("", "Not specified"),
            ("ICD-10", "ICD-10"),
            ("SNOMED CT", "SNOMED CT"),
            ("Other", "Other"),
        ],
        validators=[Optional()],
    )

    submit = SubmitField("Record Diagnosis")


class InvestigationForm(FlaskForm):
    """Form used to request a diagnostic investigation."""

    investigation_name = StringField(
        "Investigation",
        validators=[
            DataRequired(),
            Length(max=200),
        ],
    )

    category = SelectField(
        "Category",
        choices=[
            ("", "Select category"),
            ("Laboratory", "Laboratory"),
            ("Imaging", "Imaging"),
            ("Pathology", "Pathology"),
            ("Physiological", "Physiological test"),
            ("Other", "Other"),
        ],
        validators=[DataRequired()],
    )

    priority = SelectField(
        "Priority",
        choices=[
            ("Routine", "Routine"),
            ("Urgent", "Urgent"),
            ("STAT", "STAT"),
        ],
        validators=[DataRequired()],
    )

    clinical_indication = TextAreaField(
        "Clinical indication",
        validators=[
            Optional(),
            Length(max=1000),
        ],
    )

    submit = SubmitField("Order Investigation")
