from flask import Blueprint


bp = Blueprint(
    "radiation_oncology",
    __name__,
    url_prefix="/radiation-oncology",
)


from app.radiation_oncology import routes
