#!/usr/bin/python3
import unittest
from app.models.user import User


class TestUser(unittest.TestCase):
    """Test cases for the User class"""

    def test_user_creation(self):
        """Test creating a user instance."""
        user = User(first_name="John", last_name="Doe",
                    email="john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_admin)  # Default value


if __name__ == "__main__":
    unittest.main()
