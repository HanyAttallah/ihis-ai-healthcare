from flask import Blueprint


bp = Blueprint(
    "patients",
    __name__,
    url_prefix="/patients",
)


from app.patients import routes
