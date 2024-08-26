
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_testing import TestCase
from flask import Flask
from project import db
from project.models import UserModel
from testing.postgresql import Postgresql

class TestUser(TestCase):
    def create_app(self):
        test_app = Flask(__name__)
        test_app.config['TESTING'] = True
        test_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/server_portal_test'  # Replace 'testdb' with your desired test database name
        test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(test_app)  # Initialize the SQLAlchemy extension with the testing app

        return test_app

    def setUp(self):
        self.postgresql = Postgresql()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.postgresql.dsn()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        self.postgresql.stop()
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_put_valid_data(self):
        # Create a user
        user = UserModel(username='john_doe', password='password123', email='john.doe@example.com',
                    first_name='John', last_name='Doe', employee_code='EMP001', role_in_application='admin')
        db.session.add(user)
        db.session.commit()

        # Update the user's details
        response = self.client.put(f'/api/admin/user{"john_doe"}', json=dict(
            updates=dict(
                username="new_john_doe",
                password="UpdatedPassword123@",
                email="updated.john.doe@example.com",
                first_name="Updated John",
                last_name="Updated Doe",
                employee_code="EMP002",
                role_in_application="guest"
            )
        ), follow_redirects=True)

        print(response.data)
        self.assertEqual(response.status_code, 200)

        updated_user = UserModel.query.filter_by(username='new_john_doe').first()
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.password, 'UpdatedPassword123@')
        self.assertEqual(updated_user.email, 'updated.john.doe@example.com')
        self.assertEqual(updated_user.first_name, 'Updated John')
        self.assertEqual(updated_user.last_name, 'Updated Doe')
        self.assertEqual(updated_user.employee_code, 'EMP002')
        self.assertEqual(updated_user.role_in_application, 'guest')

    def test_get_user(self):
        # Create a user
        user = UserModel(username='john_doe', password='password123', email='john.doe@example.com',
                    first_name='John', last_name='Doe', employee_code='EMP001', role_in_application='admin')
        db.session.add(user)
        db.session.commit()

        # Send a GET request to retrieve the user
        response = self.client.get(f'/api/user/{user.username}')

        # Assert that the response status code is 200
        self.assert200(response)

        # Assert that the response contains the user's data
        self.assertEqual(response.json, user.json())

    def test_get_user_not_found(self):
        # Send a GET request to retrieve a non-existent user
        response = self.client.get('/api/user/nonexistent_user')

        # Assert that the response status code is 404
        self.assert404(response)

        # Assert that the response contains the appropriate message
        self.assertEqual(response.json, {'username': 'not found'})


    def test_delete_user(self):
        # Create a user
        user = UserModel(username='john_doe', password='password123', email='john.doe@example.com',
                    first_name='John', last_name='Doe', employee_code='EMP001', role_in_application='admin')
        db.session.add(user)
        db.session.commit()

        # Delete the user
        response = self.client.delete(f'/api/admin/user', json=dict(
            username="john_doe"
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(UserModel.query.filter_by(username='john_doe').first())