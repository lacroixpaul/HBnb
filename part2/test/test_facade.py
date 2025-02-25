#!/usr/bin/python3
import unittest
from app.services.facade import HBnBFacade
from app.models.place import Place
from app.models.user import User

class TestHBnBFacade(unittest.TestCase):
    def setUp(self):
        """
        This method runs before each test.
        It initializes an instance of the facade for each test case.
        """
        self.facade = HBnBFacade()

    def test_create_place_success(self):
        """
        Test the create_place function with valid data.
        """
        place_data = {
            'title': "Charming Beach House",
            'price': 150.0,
            'latitude': 34.0194,
            'longitude': -118.4912,
            'owner': User(id="123", name="John Doe"),
            'description': "Beautiful view of the ocean."
        }
        place = self.facade.create_place(place_data)
        self.assertIsInstance(place, Place)
        self.assertEqual(place.title, "Charming Beach House")

    def test_create_place_invalid_price(self):
        """
        Test create_place with an invalid price.
        """
        place_data = {
            'title': "Charming Beach House",
            'price': -50,  # Invalid price
            'latitude': 34.0194,
            'longitude': -118.4912,
            'owner': User(id="123", name="John Doe"),
            'description': "Beautiful view of the ocean."
        }
        with self.assertRaises(ValueError):
            self.facade.create_place(place_data)

    def test_get_place_success(self):
        """
        Test the get_place function with a valid ID.
        """
        place_data = {
            'title': "Mountain Cabin",
            'price': 100.0,
            'latitude': 39.7392,
            'longitude': -104.9903,
            'owner': User(id="456", name="Jane Smith"),
            'description': "Cozy cabin in the mountains."
        }
        place = self.facade.create_place(place_data)
        retrieved_place = self.facade.get_place(place.id)
        self.assertEqual(retrieved_place.title, "Mountain Cabin")

    def test_get_place_not_found(self):
        """
        Test get_place with a non-existent ID.
        """
        with self.assertRaises(ValueError):
            self.facade.get_place("invalid_id")

    def test_get_all_places(self):
        """
        Test get_all_places to check if all places are returned.
        """
        place1 = {
            'title': "City Apartment",
            'price': 200.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner': User(id="789", name="Alice Brown"),
            'description': "Modern apartment in the city center."
        }
        place2 = {
            'title': "Countryside Villa",
            'price': 300.0,
            'latitude': 51.5074,
            'longitude': -0.1278,
            'owner': User(id="101", name="Bob White"),
            'description': "Spacious villa in the countryside."
        }
        self.facade.create_place(place1)
        self.facade.create_place(place2)

        places = self.facade.get_all_places()
        self.assertEqual(len(places), 2)

    def test_update_place_success(self):
        """
        Test update_place with valid data.
        """
        place_data = {
            'title': "Old Title",
            'price': 120.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner': User(id="112", name="Charlie Black"),
            'description': "An old description."
        }
        place = self.facade.create_place(place_data)
        update_data = {
            'title': "New Title",
            'description': "A brand new description."
        }
        updated_place = self.facade.update_place(place.id, update_data)
        self.assertEqual(updated_place.title, "New Title")
        self.assertEqual(updated_place.description, "A brand new description")

    def test_update_place_not_found(self):
        """
        Test update_place with a non-existent ID.
        """
        with self.assertRaises(ValueError):
            self.facade.update_place("invalid_id", {'title': "New Title"})

if __name__ == '__main__':
    unittest.main()
