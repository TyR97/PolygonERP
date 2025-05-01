import unittest

from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from polygonerp import create_app, db
from polygonerp.models.user import User
from polygonerp.utils.auth_utils import generate_username


class UserCreationTest(TestCase):
    def create_app(self):
        app = create_app(test_config=True)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation(self):
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
                    is_admin=False
                )
        db.session.add(user)
        db.session.commit()
        fetched = User.query.filter_by(username='TesztE').first()
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "Teszt Elek")