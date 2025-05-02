from flask import Flask, redirect, url_for, Blueprint
from flask_mail import Mail

from polygonerp.controllers import dashboard_controller
from polygonerp.controllers.auth_controller import AuthController
from polygonerp.controllers.dashboard_controller import DashboardController
from polygonerp.controllers.project_controller import  ProjectController
from polygonerp.controllers.user_controller import UserController
from polygonerp.db import db, init_app

mail = Mail()

"""
    Application factory function for creating and configuring the Flask app.
    :returns: Flask app instance
"""

def create_app(testing=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = "my_secret_key"
    if testing:
        app.config.from_mapping(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            WTF_CSRF_ENABLED=False,
        )
    else:
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

    #init_project_controller(app)
    #init_user_controller(app)
    #auth_controller = AuthController(app)
    #app.register_blueprint(project_bp)
    #app.register_blueprint(user_bp)

    auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
    AuthController(auth_bp, app)
    app.register_blueprint(auth_bp)

    dash_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
    DashboardController(dash_bp, app)
    app.register_blueprint(dash_bp)

    user_bp = Blueprint('user', __name__, url_prefix='/user')
    UserController(user_bp, app)
    app.register_blueprint(user_bp)

    project_bp = Blueprint('project', __name__, url_prefix='/project')
    ProjectController(project_bp, app)
    app.register_blueprint(project_bp)




    @app.route("/")
    def index():
        return redirect(url_for('auth.login'))

    return app
