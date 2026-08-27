from flask import render_template
from flask_login import login_required

from app.auth.decorators import roles_required
from app.main import bp


@bp.route("/")
def index():
    """Render the public iHIS home page."""
    return render_template("main/home.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    """Render the authenticated iHIS dashboard."""
    return render_template("main/dashboard.html")


@bp.route("/system")
@roles_required("Administrator")
def system():
    """Administrator-only system information page."""
    return render_template("main/system.html")
