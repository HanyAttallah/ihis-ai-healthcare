from flask import Blueprint


bp = Blueprint(
    "emergency",
    __name__,
    url_prefix="/emergency",
)


from app.emergency import routes
