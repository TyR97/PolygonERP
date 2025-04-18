from flask import Flask, render_template
from flask_mail import Mail
from polygonerp.auth_controller import bp as auth_bp, init_auth_controller
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
    mail.init_app(app)
    init_app(app)

    init_auth_controller(app)
    app.register_blueprint(auth_bp)

    from polygonerp import dash
    app.register_blueprint(dash.bp)

    @app.route("/")
    def index():
        return render_template('auth/login.html')

    return app
