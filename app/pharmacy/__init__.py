from flask import Blueprint


bp = Blueprint(
    "pharmacy",
    __name__,
    url_prefix="/pharmacy",
)


from app.pharmacy import routes
