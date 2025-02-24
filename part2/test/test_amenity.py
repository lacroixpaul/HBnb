#!/usr/bin/python3
import unittest
from app.models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Test cases for the Amenity class"""

    def test_amenity_creation(self):
        """Test creating an amenity instance."""
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")


if __name__ == "__main__":
    unittest.main()
