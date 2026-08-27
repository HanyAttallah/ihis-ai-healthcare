from flask import Blueprint


bp = Blueprint(
    "clinical",
    __name__,
    url_prefix="/clinical",
)


from app.clinical import routes
