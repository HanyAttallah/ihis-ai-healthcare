from urllib.parse import urlsplit

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import bp
from app.auth.forms import LoginForm, LogoutForm
from app.extensions import db
from app.models import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate a registered iHIS user."""

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data.strip()

        user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

        if (
            user is None
            or not user.check_password(form.password.data)
            or not user.is_active
        ):
            flash("Invalid username or password.", "danger")
            return redirect(url_for("auth.login"))

        login_user(
            user,
            remember=form.remember_me.data,
        )

        next_page = request.args.get("next")

        if not next_page or urlsplit(next_page).netloc:
            next_page = url_for("main.dashboard")

        return redirect(next_page)

    return render_template(
        "auth/login.html",
        form=form,
    )


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """End the authenticated iHIS session."""

    form = LogoutForm()

    if form.validate_on_submit():
        logout_user()
        flash("You have been signed out.", "info")

    return redirect(url_for("auth.login"))
