from flask_testing import TestCase


from werkzeug.security import generate_password_hash

from polygonerp import create_app
from polygonerp.db import db
from polygonerp.models.user import User
from polygonerp.utils.auth_utils import generate_username


class AuthTestCase(TestCase):

    def create_app(self):
        app = create_app('testing')

        return app

    def setUp(self):
        # Create tables and add a test user
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

            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        # Clean up after each test
        with self.app.app_context():
            db.drop_all()

    def test_login(self):
        response = self.client.post("auth/login", data={"username": "TesztE", "password": "password", "submit": "Login"}, follow_redirects=True)
        self.assertIn(b'Welcome', response.data)

    def test_invalid_login(self):
        response = self.client.post("auth/login", data={"username": "TesztE", "password": "p4ssw0rd", "submit": "Login"}, follow_redirects=True)
        self.assertIn(b'Invalid', response.data)

    def test_register_new_user(self):
        response = self.client.post("auth/register",         data = {
            "name" : "Teszt Artúr",
            "maiden_name" : "Teszt Ellena",
            "mothers_name" : "Kis Boglárka",
            "pob" : "Budapest",
            "dob" : "1997.03.11.",
            "address" : "1102 Budapest",
            "tax_num" : "1000000001",
            "taj_number" : "123987456",
            "job_title" : "teszt",
            "base_pay" : "100",
            }, follow_redirects=True)
        self.assertIn(b'User added successfully!', response.data)










