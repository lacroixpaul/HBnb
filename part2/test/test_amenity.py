import unittest
from app.services.facade import HBnBFacade
from app.models.amenity import Amenity


class TestAmenityFacade(unittest.TestCase):

    def setUp(self):
        """Initialisation de la façade avant chaque test"""
        self.facade = HBnBFacade()

    def test_create_amenity(self):
        """Test de la création d'un équipement"""
        amenity_data = {"name": "Wi-Fi"}
        amenity = self.facade.create_amenity(amenity_data)
        self.assertEqual(amenity.name, "Wi-Fi")
        self.assertIsNotNone(amenity.id)

    def test_get_amenity(self):
        """Test de récupération d'un équipement par ID"""
        amenity_data = {"name": "Wi-Fi"}
        created_amenity = self.facade.create_amenity(amenity_data)
        retrieved_amenity = self.facade.get_amenity(created_amenity.id)
        self.assertEqual(retrieved_amenity.id, created_amenity.id)

    def test_get_all_amenities(self):
        """Test de la récupération de tous les équipements"""
        self.facade.create_amenity({"name": "Wi-Fi"})
        self.facade.create_amenity({"name": "Parking"})
        amenities = self.facade.get_all_amenities()
        self.assertEqual(len(amenities), 2)

    def test_update_amenity(self):
        """Test de mise à jour d'un équipement"""
        amenity = self.facade.create_amenity({"name": "Wi-Fi"})
        updated_amenity = self.facade.update_amenity(
            amenity.id, {"name": "Air Conditioning"})
        self.assertEqual(updated_amenity.name, "Air Conditioning")

    def test_create_amenity_duplicate(self):
        """Test de la création d'un équipement en double"""
        self.facade.create_amenity({"name": "Wi-Fi"})
        with self.assertRaises(ValueError):
            self.facade.create_amenity({"name": "Wi-Fi"})

    def test_update_amenity_empty_name(self):
        """Test de mise à jour avec un nom vide"""
        amenity = self.facade.create_amenity({"name": "Wi-Fi"})
        with self.assertRaises(ValueError):
            self.facade.update_amenity(amenity.id, {"name": ""})


if __name__ == "__main__":
    unittest.main()
