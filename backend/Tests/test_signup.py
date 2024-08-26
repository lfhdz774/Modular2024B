import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy
from project import app, db
from project.models import UserModel

class TestSignup(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db = SQLAlchemy(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_signup_post_valid_user(self):
        response = self.client.post('/api/admin/signup', json=dict(
            username="john_doe",
            password="@Securepassword-123",
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            employee_code="EMP001",
            role="admin"
        ), follow_redirects=True)

        print(response.data)
        self.assertEqual(response.status_code, 200)

        user = UserModel.query.filter_by(username='john_doe').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'john_doe')

    def test_signup_post_invalid_mail(self):
        response = self.client.post('/api/admin/signup', json=dict(
            username="john_doe",
            password="Unsecurepassword",
            email="not an email",
            first_name="John",
            last_name="Doe",
            employee_code="EMP001",
            role="admin"
        ), follow_redirects=True)

        print(response.data)
        self.assertEqual(response.status_code, 423)

    def test_signup_post_duplicate_username(self):
        # Create a user with the same username
        user = UserModel(username='john_doe', password='password123', email='john.doe@example.com',
                    first_name='John', last_name='Doe', employee_code='EMP002', role_in_application='admin')
        db.session.add(user)
        db.session.commit()

        # Try to create another user with the same username
        response = self.client.post('/api/admin/signup', json=dict(
            username="john_doe",
            password="AnotherPassword123@",
            email="another.john.doe@example.com",
            first_name="Another John",
            last_name="Doe",
            employee_code="EMP003",
            role="admin"
        ), follow_redirects=True)

        print(response.data)
        self.assertEqual(response.status_code, 424)


if __name__ == '__main__':
    unittest.main()