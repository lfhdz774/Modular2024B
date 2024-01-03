import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_testing import TestCase
from project import app, db
from project.models import UserModel

class TestLogin(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        user = UserModel(username='john_doe', password='password123', email='john.doe@example.com',
                    first_name='John', last_name='Doe', employee_code='EMP001', role_in_application='admin')
        db.session.add(user)
        db.session.commit()

        credentials = {
                'username': 'john_doe',
                'password': 'password123'
            }
        response = self.client.post('/login', json=credentials)

        print(response)
        self.assert200(response)

        # Add additional assertions to validate the login process
        self.assertIn('access_token', response.json)
        self.assertIsNotNone(response.json['access_token'])

    def test_wrong_password(self):
        user = UserModel(username='john_doe', password='password123', email='john.doe@example.com',
                    first_name='John', last_name='Doe', employee_code='EMP001', role_in_application='admin')
        db.session.add(user)
        db.session.commit()

        credentials = {
                'username': 'john_doe',
                'password': 'wrong_password'
            }
        response = self.client.post('/login', json=credentials)

        self.assert401(response)
        self.assertNotIn('access_token', response.json)

    

    