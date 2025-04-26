from flask import Flask, redirect, url_for, Blueprint
from flask_mail import Mail
from polygonerp.auth_controller import bp as auth_bp, init_auth_controller
from polygonerp.dashboard_controller import DashboardController
from polygonerp.db import db, init_app

mail = Mail()

"""
    Application factory function for creating and configuring the Flask app.
    :returns: Flask app instance
"""

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = "my_secret_key"

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///polygoner.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAIL_SERVER="smtp.mailgun.org",
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME="",
        MAIL_PASSWORD="",
    )

    #Init db and mail
    from polygonerp.models.user import User
    from polygonerp.models.time_log import TimeLog
    from polygonerp.models.project import Project

    mail.init_app(app)
    init_app(app)

    init_auth_controller(app)
    app.register_blueprint(auth_bp)

    dash_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
    DashboardController(dash_bp, app)
    app.register_blueprint(dash_bp)

    with app.app_context():
        pass


    @app.route("/")
    def index():
        return redirect(url_for('auth.login'))

    return app
