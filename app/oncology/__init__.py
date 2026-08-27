from flask import Blueprint


bp = Blueprint(
    "oncology",
    __name__,
    url_prefix="/oncology",
)


from app.oncology import routes
