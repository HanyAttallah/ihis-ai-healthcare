from flask import render_template

from app.education import bp
from app.education.forms import PatientQuestionForm
from app.services.ai.patient_education import (
    answer_patient_question,
)


@bp.route(
    "/assistant",
    methods=["GET", "POST"],
)
def assistant():
    form = PatientQuestionForm()
    result = None

    if form.validate_on_submit():
        result = answer_patient_question(
            form.question.data.strip()
        )

    return render_template(
        "education/assistant.html",
        form=form,
        result=result,
    )
