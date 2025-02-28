import unittest
from app.models.place import Place
from app.models.user import User


class TestPlaceModel(unittest.TestCase):
    """Unit tests for the Place model."""

    def setUp(self):
        """Set up a sample User and Place instance before each test."""
        # Create a test user first
        self.test_user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )
        self.user_id = self.test_user.id  # Retrieve the UUID

        # Create a test place using the generated user_id
        self.valid_place = Place(
            title="Cozy Apartment",
            price=120.0,
            latitude=45.764043,
            longitude=4.835659,
            owner_id=self.user_id,  # Use the correct user_id
            description="A nice place in the city center"
        )

    def test_place_creation_success(self):
        """Test that a Place instance is correctly created with valid data."""
        self.assertEqual(self.valid_place.title, "Cozy Apartment")
        self.assertEqual(self.valid_place.price, 120.0)
        self.assertEqual(self.valid_place.latitude, 45.764043)
        self.assertEqual(self.valid_place.longitude, 4.835659)
        self.assertEqual(self.valid_place.owner_id,
                         self.user_id)  # Check owner_id match
        self.assertEqual(self.valid_place.description,
                         "A nice place in the city center")

    def test_place_creation_missing_title(self):
        """Test that creating a Place without a title raises a ValueError."""
        with self.assertRaises(ValueError):
            Place(
                title="",
                price=100.0,
                latitude=44.5,
                longitude=10.5,
                owner_id=self.user_id
            )

    def test_place_creation_missing_owner(self):
        """Test that creating a Place without an owner_id raises a ValueError."""
        with self.assertRaises(ValueError):
            Place(
                title="Nice House",
                price=80.0,
                latitude=40.0,
                longitude=-75.0,
                owner_id=None
            )

    def test_place_creation_negative_price(self):
        """Test that setting a negative price raises a ValueError."""
        with self.assertRaises(ValueError):
            Place(
                title="Budget Room",
                price=-50.0,
                latitude=37.7749,
                longitude=-122.4194,
                owner_id=self.user_id
            )

    def test_place_creation_invalid_latitude(self):
        """Test that an invalid latitude value raises a ValueError."""
        with self.assertRaises(ValueError):
            Place(
                title="Mountain Cabin",
                price=150.0,
                latitude=100.0,  # Invalid latitude
                longitude=10.0,
                owner_id=self.user_id
            )

    def test_place_creation_invalid_longitude(self):
        """Test that an invalid longitude value raises a ValueError."""
        with self.assertRaises(ValueError):
            Place(
                title="Lakeside House",
                price=90.0,
                latitude=50.0,
                longitude=-190.0,  # Invalid longitude
                owner_id=self.user_id
            )

    def test_to_dict_method(self):
        """Test that the to_dict method returns the correct dictionary representation."""
        place_dict = self.valid_place.to_dict()
        self.assertEqual(place_dict["title"], "Cozy Apartment")
        self.assertEqual(place_dict["price"], 120.0)
        self.assertEqual(place_dict["latitude"], 45.764043)
        self.assertEqual(place_dict["longitude"], 4.835659)
        # Verify UUID consistency
        self.assertEqual(place_dict["owner_id"], self.user_id)
        self.assertEqual(place_dict["description"],
                         "A nice place in the city center")
        self.assertIn("created_at", place_dict)
        self.assertIn("updated_at", place_dict)

    def test_add_review(self):
        """Test that a review can be added to a Place instance."""
        self.valid_place.add_review("Great stay!")
        self.assertEqual(len(self.valid_place.reviews), 1)
        self.assertEqual(self.valid_place.reviews[0], "Great stay!")

    def test_add_amenity(self):
        """Test that an amenity can be added to a Place instance."""
        self.valid_place.add_amenity("WiFi")
        self.assertEqual(len(self.valid_place.amenities), 1)
        self.assertEqual(self.valid_place.amenities[0], "WiFi")


if __name__ == "__main__":
    unittest.main()
