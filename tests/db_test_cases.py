from datetime import datetime
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from polygonerp import create_app
from polygonerp.db import db
from polygonerp.models.project import Project
from polygonerp.models.user import User
from polygonerp.utils.auth_utils import generate_username

class DBTestCase(TestCase):

    def create_app(self):
        app = create_app('testing')  # Set the config to testing mode

        return app

    """
        Creating tables and adding test user
    """
    def setUp(self):

        with self.app.app_context():
            db.create_all()

            user = User(
                username=generate_username([], "Teszt Elek"),
                password_hash=generate_password_hash("password"),
                name="Teszt Elek",
                maiden_name="",
                mothers_name="Teszt Ellena",
                pob="Budapest",
                dob="1997.03.11.",
                address="Teszt cím",
                tax_num="0000000001",
                taj_number="000000001",
                job_title="teszt",
                base_pay="100",
                email_address="TesztE@polygon_erp.com",
                is_admin=False,
                first_login=False
            )
            project = Project(
                name="Test Project",
                start_date=datetime.strptime("2020-01-02", "%Y-%m-%d").date(),
                finish_date=datetime.strptime("2020-01-03", "%Y-%m-%d").date(),
                supervisor_id=1
            )
            db.session.add(project)
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_create_user_same_name(self):
        user = User(
            username=generate_username(["TesztE"], "Teszt Elek"),
            password_hash=generate_password_hash("password"),
            name="Teszt Elek",
            maiden_name="",
            mothers_name="Teszt Ellena",
            pob="Budapest",
            dob="1997.03.11.",
            address="Teszt cím",
            tax_num="0000000002",
            taj_number="000000002",
            job_title="teszt",
            base_pay="100",
            email_address="TesztE@polygon_erp.com",
            is_admin=False,
            first_login=False
        )

        db.session.add(user)
        db.session.commit()

        self.assertIsNotNone(User.query.filter_by(username="TesztE1"))


    def test_delete_user(self):
        user = User.query.filter_by(username="TesztE").first()

        db.session.delete(user)
        db.session.commit()

        self.assertIsNone(User.query.filter_by(username="TesztE").first())