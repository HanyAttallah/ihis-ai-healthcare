from flask import Flask

from app.extensions import csrf, db, login_manager, migrate
from config import Config


def create_app(config_class=Config):
    """Create and configure the iHIS Flask application."""

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app import models

    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    csrf.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.patients import bp as patients_bp
    app.register_blueprint(patients_bp)

    from app.clinical import bp as clinical_bp
    app.register_blueprint(clinical_bp)

    from app.receptionist import bp as receptionist_bp
    app.register_blueprint(receptionist_bp)

    from app.gp import bp as gp_bp
    app.register_blueprint(gp_bp)

    from app.icu import bp as icu_bp
    app.register_blueprint(icu_bp)

    from app.imaging import bp as imaging_bp
    app.register_blueprint(imaging_bp)

    from app.education import bp as education_bp
    app.register_blueprint(education_bp)

    from app.pharmacy import bp as pharmacy_bp
    app.register_blueprint(pharmacy_bp)

    from app.mental_health import bp as mental_health_bp
    app.register_blueprint(mental_health_bp)


    from app.reasoning import bp as reasoning_bp
    app.register_blueprint(reasoning_bp)

    from app.emergency import bp as emergency_bp
    app.register_blueprint(emergency_bp)

    from app.oncology import bp as oncology_bp
    app.register_blueprint(oncology_bp)

    from app.multi_agent import bp as multi_agent_bp
    app.register_blueprint(multi_agent_bp)

    from app.radiation_oncology import bp as radiation_oncology_bp
    app.register_blueprint(radiation_oncology_bp)

    from app.auth.forms import LogoutForm

    @app.context_processor
    def inject_logout_form():
        """Make the CSRF-protected logout form available globally."""

        return {
            "logout_form": LogoutForm(),
        }

    return app


