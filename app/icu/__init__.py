from flask import Blueprint


bp = Blueprint(
    "icu",
    __name__,
    url_prefix="/icu",
)


from app.icu import routes
