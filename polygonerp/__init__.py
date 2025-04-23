from flask import Flask, redirect, url_for, Blueprint
from flask_mail import Mail
from polygonerp.auth_controller import bp as auth_bp, init_auth_controller
from polygonerp.dashboard import DashboardController
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
        MAIL_USERNAME="postmaster@sandbox0ce297070b444e6ea390aba06950b419.mailgun.org",
        MAIL_PASSWORD="825f1c7c1c17ffb135649d15f4562a16-f6202374-9458f4bc",
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
        from datetime import date

        # Get existing users
        supervisor = User.query.get(3)  # assuming user with id=1 exists
        worker1 = User.query.get(2)   # assuming user with id=2 exists   # assuming user with id=2 exists

        if supervisor and worker1:
            # Create new project
            new_project = Project(
                name="Dildo tester",
                start_date=date.today(),
                finish_date=date(2025, 8, 18),
                supervisor_id=supervisor.id,
                assigned_workers=[worker1]  # you can add more workers here
            )

            db.session.add(new_project)
            db.session.commit()
            print("✅ Project created and users assigned.")
        else:
            print("⚠️ Supervisor or worker user not found.")


    @app.route("/")
    def index():
        return redirect(url_for('auth.login'))

    return app
