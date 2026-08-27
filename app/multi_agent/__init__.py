from flask import Blueprint

bp = Blueprint(
    "multi_agent",
    __name__,
    url_prefix="/multi-agent",
)

from app.multi_agent import routes
