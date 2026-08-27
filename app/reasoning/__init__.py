from flask import Blueprint


bp = Blueprint(
    "reasoning",
    __name__,
    url_prefix="/reasoning",
)


from app.reasoning import routes
