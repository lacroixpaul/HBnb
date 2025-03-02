import unittest
import uuid
from app.models.user import User
from app.services.facade import HBnBFacade
from app.persistence.repository import InMemoryRepository


class TestUserFacade(unittest.TestCase):
    """
    Unit tests for the User model.

    === Setup ===
        - setUp(self): Initializes the UserFacade and creates a test user.

    === Testing user creation ===
        - test_01_create_user_success(self): Valid user creation.
        - test_02_create_user_missing_fields(self): Missing required fields.
        - test_03_create_user_duplicate_email(self): Attempt to create a user with an already used email.

    === Testing get_user method ===
        - test_04_get_all_users(self): Retrieve all users
        - test_05_get_user_success(self): Retrieve a user by ID.
        - test_06_get_user_not_found(self): Retrieve a user with an invalid/non-existent ID.

    === Testing update_user method ===
        - test_07_update_user_success(self): Updating user with valid data.
        - test_08_update_user_invalid_fields(self): Updating user with invalid fields (e.g., malformed email).
        - test_09_update_user_duplicate_email(self): Attempt to update a user's email with one that is already used.
    """

    def setUp(self):
        self.facade = HBnBFacade()
        self.facade.user_repo = InMemoryRepository()

        self.user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        self.test_user = self.facade.create_user(self.user_data)

    def test_01_create_user_success(self):
        """Test creating a valid user."""
        self.assertIsInstance(self.test_user.id, str)
        self.assertEqual(self.test_user.first_name, "John")

    def test_02_create_user_missing_fields(self):
        """Test creating a user with missing fields."""
        with self.assertRaises(ValueError):
            self.facade.create_user({"first_name": "Alice"})

    def test_03_create_user_duplicate_email(self):
        """Test creating a user with an already used email."""
        with self.assertRaises(ValueError):
            self.facade.create_user(self.user_data)

    def test_04_get_all_users(self):
        """Test retrieving all users"""
        self.facade.user_repo = InMemoryRepository()
        users_before = self.facade.get_all_users()

        self.facade.create_user(
            {"first_name": "Alice", "last_name": "Brown", "email": "alice@example.com"})
        self.facade.create_user(
            {"first_name": "Bob", "last_name": "Johnson", "email": "bob@example.com"})

        users = self.facade.get_all_users()
        print("Users after adding:", len(users))  # Debug

        # Vérifie qu'il n'y a bien que 2 utilisateurs
        self.assertEqual(len(users), 2)

    def clear_users(self):
        """Supprime tous les utilisateurs du dépôt (utile pour les tests)."""
        self.user_repo = InMemoryRepository()

    def test_05_get_user_success(self):
        """Test retrieving a valid user."""
        user = self.facade.get_user(self.test_user.id)
        self.assertEqual(user.email, "john.doe@example.com")

    def test_06_get_user_not_found(self):
        """Test retrieving a non-existent user."""
        with self.assertRaises(ValueError):
            # Random ID that doesn't exist
            self.facade.get_user(str(uuid.uuid4()))

    def test_07_update_user_success(self):
        """Test updating a user with valid data."""
        updated_user = self.facade.update_user(
            self.test_user.id, {"first_name": "Jane"})
        self.assertEqual(updated_user.first_name, "Jane")

    def test_08_update_user_invalid_fields(self):
        """Test updating a user with invalid fields."""
        with self.assertRaises(ValueError):
            self.facade.update_user(
                self.test_user.id, {"email": "invalid-email"})

    def test_09_update_user_duplicate_email(self):
        """Test that updating a user with an already used email fails."""
        # Create two distinct users
        user1_data = {
            "first_name": "Alice",
            "last_name": "Brown",
            "email": "alice@example.com"
        }
        user2_data = {
            "first_name": "Bob",
            "last_name": "Johnson",
            "email": "bob@example.com"
        }

        user1 = self.facade.create_user(user1_data)
        user2 = self.facade.create_user(user2_data)

        # 🚨 Attempt to update user2's email to match user1's email
        with self.assertRaises(ValueError) as context:
            self.facade.update_user(user2.id, {"email": user1.email})

        self.assertEqual(str(context.exception), "Email already in use")


if __name__ == "__main__":
    unittest.main()
