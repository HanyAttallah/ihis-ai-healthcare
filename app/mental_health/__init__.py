from flask import Blueprint


bp = Blueprint(
    "mental_health",
    __name__,
    url_prefix="/mental-health",
)


from app.mental_health import routes
