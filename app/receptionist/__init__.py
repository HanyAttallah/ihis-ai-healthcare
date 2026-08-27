from flask import Blueprint


bp = Blueprint(
    "receptionist",
    __name__,
    url_prefix="/receptionist",
)


from app.receptionist import routes
