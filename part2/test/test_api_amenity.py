import unittest
import json
from app import create_app
from app.services.facade import HBnBFacade


class TestAmenityAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialisation unique pour l'ensemble des tests"""
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        cls.facade = HBnBFacade()

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        cls.app_context.pop()

    def test_create_amenity_api(self):
        """Test de l'endpoint POST /api/v1/amenities/"""
        response = self.client.post(
            '/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        # Vérifie que la réponse est bien structurée
        self.assertIsNotNone(data)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Wi-Fi")

    def test_get_all_amenities_api(self):
        """Test de l'endpoint GET /api/v1/amenities/"""
        self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.client.post('/api/v1/amenities/', json={"name": "Parking"})

        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, list)
        # Vérifie qu'il y a au moins 2 équipements
        self.assertGreaterEqual(len(data), 2)

    def test_get_amenity_by_id_api(self):
        """Test de l'endpoint GET /api/v1/amenities/<id>"""
        post_response = self.client.post(
            '/api/v1/amenities/', json={"name": "Wi-Fi"})
        data = post_response.get_json()

        self.assertIsNotNone(data)  # Vérifie que la réponse n'est pas vide
        self.assertIn('id', data)   # Assure que l'ID est bien présent

        self.assertIsNotNone(data)  # Vérifie la réponse de création
        self.assertIn('id', data)

        amenity_id = data['id']
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data['id'], amenity_id)

    def test_update_amenity_api(self):
        """Test de l'endpoint PUT /api/v1/amenities/<id>"""
        post_response = self.client.post(
            '/api/v1/amenities/', json={"name": "Wi-Fi"})
        data = post_response.get_json()

        self.assertIsNotNone(data)
        self.assertIn('id', data)

        amenity_id = data['id']
        put_response = self.client.put(
            f'/api/v1/amenities/{amenity_id}', json={"name": "Air Conditioning"})

        self.assertEqual(put_response.status_code, 200)

        data = put_response.get_json()
        self.assertIsNotNone(data)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Air Conditioning")

    def test_create_duplicate_amenity_api(self):
        """Test de création d'un équipement en double"""
        self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        response = self.client.post(
            '/api/v1/amenities/', json={"name": "Wi-Fi"})

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "Amenity already exist.")

    def test_update_amenity_empty_name_api(self):
        """Test de mise à jour avec un nom vide"""
        post_response = self.client.post(
            '/api/v1/amenities/', json={"name": "Wi-Fi"})
        data = post_response.get_json()

        self.assertIsNotNone(data)
        self.assertIn('id', data)

        amenity_id = data['id']
        put_response = self.client.put(
            f'/api/v1/amenities/{amenity_id}', json={"name": ""})

        self.assertEqual(put_response.status_code, 400)

        data = put_response.get_json()
        self.assertIsNotNone(data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "Amenity name cannot be empty.")


if __name__ == "__main__":
    unittest.main()
