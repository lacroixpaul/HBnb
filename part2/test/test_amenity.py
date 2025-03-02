import unittest
import uuid
from app.services.facade import HBnBFacade
from app.models.amenity import Amenity
from werkzeug.exceptions import NotFound


class TestAmenityFacade(unittest.TestCase):
    """
    Unit tests for the Amenity model.

    === Setup ===
        - setUp(self): Initializes the test environment and creates an instance of the AmenityFacade.

    === Testing amenity creation ===
        - test_01_create_amenity_success(self): Valid amenity creation.
        - test_02_create_amenity_duplicate(self): Attempt to create a duplicate amenity.

    === Testing get_amenity method ===
        - test_03_get_amenity_success(self): Retrieve an amenity by ID.
        - test_04_get_amenity_not_found(self): Retrieve an amenity with an invalid/non-existent ID.

    === Testing get_all_amenities method ===
        - test_05_get_all_amenities(self): Retrieve all amenities.

    === Testing update_amenity method ===
        - test_06_update_amenity_success(self): Updating an amenity with valid data.
        - test_07_update_amenity_empty_name(self): Attempting to update an amenity with an empty name.
        - test_08_update_amenity_not_found(self): Attempting to update a non-existent amenity.
    """

    def setUp(self):
        """Initialisation de la façade avant chaque test"""
        self.facade = HBnBFacade()

    def test_01_create_amenity_success(self):
        """Test de la création d'un équipement"""
        amenity_data = {"name": "Wi-Fi"}
        amenity = self.facade.create_amenity(amenity_data)
        self.assertEqual(amenity.name, "Wi-Fi")
        self.assertIsNotNone(amenity.id)

    def test_02_create_amenity_duplicate(self):
        """Test de la création d'un équipement en double"""
        self.facade.create_amenity({"name": "Wi-Fi"})
        with self.assertRaises(ValueError):
            self.facade.create_amenity({"name": "Wi-Fi"})

    def test_03_get_amenity_success(self):
        """Test de récupération d'un équipement par ID"""
        amenity_data = {"name": "Wi-Fi"}
        created_amenity = self.facade.create_amenity(amenity_data)
        retrieved_amenity = self.facade.get_amenity(created_amenity.id)
        self.assertEqual(retrieved_amenity.id, created_amenity.id)

    def test_04_get_amenity_not_found(self):
        """Test retrieving an amenity with a non-existent ID."""
        with self.assertRaises(NotFound) as context:
            self.facade.get_amenity(str(uuid.uuid4()))
        self.assertEqual(str(context.exception.description),
                         "Amenity not found")

    def test_05_get_all_amenities(self):
        """Test de la récupération de tous les équipements"""
        self.facade.create_amenity({"name": "Wi-Fi"})
        self.facade.create_amenity({"name": "Parking"})
        amenities = self.facade.get_all_amenities()
        self.assertEqual(len(amenities), 2)

    def test_06_update_amenity_success(self):
        """Test de mise à jour d'un équipement"""
        amenity = self.facade.create_amenity({"name": "Wi-Fi"})
        updated_amenity = self.facade.update_amenity(
            amenity.id, {"name": "Air Conditioning"})
        self.assertEqual(updated_amenity.name, "Air Conditioning")

    def test_07_update_amenity_empty_name(self):
        """Test de mise à jour avec un nom vide"""
        amenity = self.facade.create_amenity({"name": "Wi-Fi"})
        with self.assertRaises(ValueError):
            self.facade.update_amenity(amenity.id, {"name": ""})

    def test_08_update_amenity_not_found(self):
        """Test updating an amenity that does not exist."""
        with self.assertRaises(NotFound) as context:
            self.facade.update_amenity(str(uuid.uuid4()), {"name": "Pool"})

        self.assertEqual(str(context.exception.description),
                         "Amenity not found")  # Vérification correcte


if __name__ == "__main__":
    unittest.main()
