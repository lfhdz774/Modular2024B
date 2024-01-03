
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_testing import TestCase
from project import app, db
from project.models import UserModel

class TestUser(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_put_valid_data(self):
        # Create a user
        user = UserModel(username='john_doe', password='password123', email='john.doe@example.com',
                    first_name='John', last_name='Doe', employee_code='EMP001', role_in_application='admin')
        db.session.add(user)
        db.session.commit()

        # Update the user's details
        response = self.client.put(f'/user', json=dict(
            username="john_doe",
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

    def test_get_specific_user(self):
        # Create a user
        user = UserModel(username='john_doe', password='password123', email='john.doe@example.com',
                    first_name='John', last_name='Doe', employee_code='EMP001', role_in_application='admin')
        db.session.add(user)
        db.session.commit()

        # Get the specific user
        response = self.client.get(f'/user', json=dict(
                        username="john_doe") , follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'john_doe')
        self.assertEqual(response.json['email'], 'john.doe@example.com')
        self.assertEqual(response.json['first_name'], 'John')
        self.assertEqual(response.json['last_name'], 'Doe')
        self.assertEqual(response.json['employee_code'], 'EMP001')
        self.assertEqual(response.json['role_in_application'], 'admin')


    def test_delete_user(self):
        # Create a user
        user = UserModel(username='john_doe', password='password123', email='john.doe@example.com',
                    first_name='John', last_name='Doe', employee_code='EMP001', role_in_application='admin')
        db.session.add(user)
        db.session.commit()

        # Delete the user
        response = self.client.delete(f'/user', json=dict(
            username="john_doe"
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(UserModel.query.filter_by(username='john_doe').first())