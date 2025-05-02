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
        Creating tables and adding test user and test project
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

    def test_project_list_with_existing_project(self):
        response = self.client.get('/project/list_projects')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Project', response.data)

    def test_project_list_with_empty_project(self):
        project = Project.query.filter_by(name="Test Project").first()
        db.session.delete(project)
        db.session.commit()
        response = self.client.get('/project/list_projects')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No projects found!', response.data)

