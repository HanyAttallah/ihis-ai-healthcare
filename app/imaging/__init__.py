from flask import Blueprint


bp = Blueprint(
    "imaging",
    __name__,
    url_prefix="/imaging",
)


from app.imaging import routes
