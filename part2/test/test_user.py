import unittest
from app.services.facade import HBnBFacade
from app.models.user import User


class TestUserFacade(unittest.TestCase):

    def setUp(self):
        """Initialize the Facade before each test"""
        self.facade = HBnBFacade()

    def test_create_user_success(self):
        """Test creating a valid user"""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        created_user = self.facade.create_user(user_data)

        self.assertIsInstance(created_user, User)
        self.assertEqual(created_user.first_name, "John")
        self.assertEqual(created_user.last_name, "Doe")
        self.assertEqual(created_user.email, "john.doe@example.com")
        # ✅ Vérifie que l'UUID est bien généré
        self.assertIsNotNone(created_user.id)

    def test_create_user_duplicate_email(self):
        """Test creating a user with a duplicate email"""
        user_data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com"
        }
        self.facade.create_user(user_data)

        # 🚨 Vérifie que la duplication est bloquée
        with self.assertRaises(ValueError):
            self.facade.create_user(user_data)

    def test_create_user_missing_fields(self):
        """Test creating a user with missing fields"""
        user_data = {"first_name": "Charlie"}

        with self.assertRaises(ValueError):
            self.facade.create_user(user_data)

    def test_get_user_success(self):
        """Test retrieving a valid user"""
        user_data = {
            "first_name": "Eve",
            "last_name": "Miller",
            "email": "eve.miller@example.com"
        }
        created_user = self.facade.create_user(user_data)
        retrieved_user = self.facade.get_user(created_user.id)

        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, created_user.id)
        self.assertEqual(retrieved_user.email, "eve.miller@example.com")

    def test_get_user_not_found(self):
        """Test retrieving a non-existent user"""
        retrieved_user = self.facade.get_user("invalid_uuid")
        self.assertIsNone(retrieved_user)

    def test_get_all_users(self):
        """Test retrieving all users"""
        self.facade.create_user(
            {"first_name": "Alice", "last_name": "Brown", "email": "alice@example.com"})
        self.facade.create_user(
            {"first_name": "Bob", "last_name": "Johnson", "email": "bob@example.com"})

        users = self.facade.get_all_users()
        self.assertEqual(len(users), 2)

    def test_update_user_success(self):
        """Test updating a valid user"""
        user_data = {
            "first_name": "Lucas",
            "last_name": "White",
            "email": "lucas.white@example.com"
        }
        created_user = self.facade.create_user(user_data)
        user_id = created_user.id

        update_data = {
            "first_name": "Luke",
            "last_name": "W.",
            "email": "luke.w@example.com"
        }
        updated_user = self.facade.update_user(user_id, update_data)

        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.id, user_id)
        self.assertEqual(updated_user.first_name, "Luke")
        self.assertEqual(updated_user.last_name, "W.")
        self.assertEqual(updated_user.email, "luke.w@example.com")

    def test_update_user_not_found(self):
        """Test updating a non-existent user"""
        update_data = {
            "first_name": "Nina",
            "last_name": "Black",
            "email": "nina@example.com"
        }
        updated_user = self.facade.update_user(
            "invalid_uuid", update_data)

        self.assertIsNone(updated_user)

    def test_update_user_invalid_fields(self):
        """Test updating a user with invalid fields"""
        user_data = {
            "first_name": "Sam",
            "last_name": "Fisher",
            "email": "sam@example.com"
        }
        created_user = self.facade.create_user(user_data)
        user_id = created_user.id

        update_data = {"email": "not_an_email"}

        with self.assertRaises(ValueError):
            self.facade.update_user(user_id, update_data)


if __name__ == '__main__':
    unittest.main()
