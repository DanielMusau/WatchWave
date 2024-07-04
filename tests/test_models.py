import unittest
from app import create_app, db
from app.models import User, Account
from werkzeug.security import generate_password_hash
from config import TestingConfig
from sqlalchemy.sql import func

class ModelsTestCase(unittest.TestCase):
    """
    This class represents the test cases for the database models.
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

    def test_user_creation(self):
        """
        This method tests the creation of a user.
        """
        with self.app.app_context():
            password_hash = generate_password_hash('testpassword')
            user = User(
                username='testuser',
                email='testuser@example.com',
                password_hash=password_hash,
                created_at=func.now(),
                updated_at=func.now()
            )
            db.session.add(user)
            db.session.commit()

            retrieved_user = User.query.filter_by(email='testuser@example.com').first()
            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user.username, 'testuser')
            self.assertEqual(retrieved_user.email, 'testuser@example.com')
            self.assertEqual(retrieved_user.password_hash, password_hash)

    def test_account_creation(self):
        """
        This method tests the creation of an account.
        """
        with self.app.app_context():
            password_hash = generate_password_hash('testpassword')
            user = User(
                username='testuser',
                email='testuser@example.com',
                password_hash=password_hash,
                created_at=func.now(),
                updated_at=func.now()
            )
            db.session.add(user)
            db.session.commit()

            account = Account(
                email=user.email,
                user_id=user.id,
                created_at=func.now(),
                updated_at=func.now()
            )
            db.session.add(account)
            db.session.commit()

            retrieved_account = Account.query.filter_by(email='testuser@example.com').first()
            self.assertIsNotNone(retrieved_account)
            self.assertEqual(retrieved_account.user_id, user.id)
            self.assertEqual(retrieved_account.email, user.email)


if __name__ == '__main__':
    unittest.main()