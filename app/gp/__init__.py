from flask import Blueprint


bp = Blueprint(
    "gp",
    __name__,
    url_prefix="/gp",
)


from app.gp import routes
