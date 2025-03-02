import unittest
from app.services.facade import HBnBFacade
from app.models.user import User
from app.models.place import Place
import uuid


class TestPlaceFacade(unittest.TestCase):

    def setUp(self):
        """Initialize the Facade and create a test User & Place"""
        self.facade = HBnBFacade()

        # :one: Create a test user with a valid UUID
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com"
        }
        self.test_user = self.facade.create_user(user_data)

        # :two: Ensure the user is properly created with an ID
        self.assertIsInstance(uuid.UUID(self.test_user.id), uuid.UUID)
        self.assertEqual(self.test_user.first_name, "Test")
        self.assertEqual(self.test_user.last_name, "User")

        # :three: Create a test place linked to this user
        place_data = {
            "title": "Test Place",
            "description": "A place for testing",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            # Utilisation de l'ID de l'utilisateur, pas de l'objet complet
            "owner_id": str(self.test_user.id)
        }
        self.test_place = self.facade.create_place(place_data)

        # :four: Verify that the place is correctly created and has the user as the owner by ID
        # Vérifie que l'owner_id est bien l'ID de l'utilisateur
        self.assertEqual(self.test_place.owner_id, str(self.test_user.id))

    def test_create_place(self):
        """Test that the place was created properly"""
        self.assertEqual(self.test_place.title, "Test Place")
        self.assertEqual(self.test_place.price, 100.0)
        self.assertEqual(self.test_place.latitude, 40.7128)
        self.assertEqual(self.test_place.longitude, -74.0060)
        # Vérifie que l'owner_id est correct
        self.assertEqual(self.test_place.owner_id, str(self.test_user.id))


if __name__ == "__main__":
    unittest.main()
