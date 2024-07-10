import unittest
from app import create_app, db
from app.models import User, Account
from werkzeug.security import generate_password_hash
from config import TestingConfig
from sqlalchemy.sql import func


class RoutesTestCase(unittest.TestCase):
    """
    This class represents the test cases for the routes.
    """

    def setUp(self):
        """
        This method sets up the test client and the test database.
        """
        self.app = create_app()
        self.app.config.from_object(TestingConfig)
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        This method removes the test database and the test client.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup(self):
        """
        This method tests the signup route.
        """
        response = self.client().post(
            "/api/signup",
            json={
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "testpassword",
            },
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", data)
        self.assertEqual(data["email"], "testuser@example.com")

    def test_login(self):
        """
        This method tests the login route.
        """
        with self.app.app_context():
            password_hash = generate_password_hash("testpassword")
            user = User(
                username="testuser",
                email="testuser@example.com",
                password_hash=password_hash,
                created_at=func.now(),
                updated_at=func.now(),
            )
            db.session.add(user)
            db.session.commit()

            new_account = Account(
                email=user.email,
                user_id=user.id,
                created_at=func.now(),
                updated_at=func.now(),
            )

            db.session.add(new_account)
            db.session.commit()

        response = self.client().post(
            "/api/login",
            json={"email": "testuser@example.com", "password": "testpassword"},
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", data)
        self.assertIn("account", data)
        self.assertEqual(data["account"]["email"], "testuser@example.com")

    def test_login_invalid_data(self):
        """
        This method tests the login route with invalid data.
        """
        response = self.client().post(
            "/api/login",
            json={"email": "wrongemail@example.com", "password": "wrongpassword"},
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid credentials")


if __name__ == "__main__":
    unittest.main()
