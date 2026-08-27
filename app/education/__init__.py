from flask import Blueprint


bp = Blueprint(
    "education",
    __name__,
    url_prefix="/education",
)


from app.education import routes
