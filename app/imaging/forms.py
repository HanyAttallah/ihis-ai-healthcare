from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField


class XRayUploadForm(FlaskForm):
    image = FileField(
        "Upload X-ray image",
        validators=[
            FileRequired(),
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Upload a JPG or PNG image.",
            ),
        ],
    )

    submit = SubmitField(
        "Analyze X-ray"
    )
