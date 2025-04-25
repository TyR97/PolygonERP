from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
  Initializes the database and binds it to the Flask application

  :return: None
  :rtype: None
"""


def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()






