from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class ReceptionistIntakeForm(FlaskForm):
    """Structured administrative symptom intake for routing support."""

    symptom_text = TextAreaField(
        "Reported symptoms / reason for visit",
        validators=[
            DataRequired(),
            Length(max=2000),
        ],
    )

    symptom_duration = StringField(
        "Symptom duration",
        validators=[
            Optional(),
            Length(max=120),
        ],
    )

    additional_context = TextAreaField(
        "Additional non-diagnostic context",
        validators=[
            Optional(),
            Length(max=1000),
        ],
    )

    submit = SubmitField(
        "Analyze Intake",
    )


class AIReviewForm(FlaskForm):
    """Human oversight form for a receptionist AI assessment."""

    decision = SelectField(
        "Review decision",
        choices=[
            ("", "Select decision"),
            ("Accepted", "Accept AI recommendation"),
            ("Modified", "Modify AI recommendation"),
            ("Rejected", "Reject AI recommendation"),
        ],
        validators=[
            DataRequired(),
        ],
    )

    final_service = SelectField(
        "Final service",
        choices=[
            ("", "Not applicable / select service"),
            ("Emergency Department", "Emergency Department"),
            ("General Medicine", "General Medicine"),
            ("Respiratory Medicine", "Respiratory Medicine"),
            ("Cardiology", "Cardiology"),
            ("Neurology", "Neurology"),
            ("Gastroenterology", "Gastroenterology"),
            ("Orthopedics", "Orthopedics"),
            ("Dermatology", "Dermatology"),
        ],
        validators=[
            Optional(),
        ],
    )

    final_urgency = SelectField(
        "Final urgency",
        choices=[
            ("", "Not applicable / select urgency"),
            ("Routine", "Routine"),
            ("Prompt", "Prompt"),
            ("Emergency", "Emergency"),
        ],
        validators=[
            Optional(),
        ],
    )

    comments = TextAreaField(
        "Review comments",
        validators=[
            Optional(),
            Length(max=2000),
        ],
    )

    submit = SubmitField(
        "Submit Human Review",
    )

    def validate(self, extra_validators=None):
        """Apply decision-specific review requirements."""

        if not super().validate(
            extra_validators=extra_validators
        ):
            return False

        valid = True

        if self.decision.data == "Modified":
            if not self.final_service.data:
                self.final_service.errors.append(
                    "Select the final service when modifying "
                    "the AI recommendation."
                )
                valid = False

            if not self.final_urgency.data:
                self.final_urgency.errors.append(
                    "Select the final urgency when modifying "
                    "the AI recommendation."
                )
                valid = False

            if not (
                self.comments.data
                and self.comments.data.strip()
            ):
                self.comments.errors.append(
                    "Explain why the AI recommendation "
                    "was modified."
                )
                valid = False

        if self.decision.data == "Rejected":
            if not (
                self.comments.data
                and self.comments.data.strip()
            ):
                self.comments.errors.append(
                    "Explain why the AI recommendation "
                    "was rejected."
                )
                valid = False

        return valid

