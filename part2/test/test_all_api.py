import unittest
import json
from app import create_app


class TestUserPlaceReviewEndpoints(unittest.TestCase):
    """
    Unit tests for User, Place, and Review endpoints using Flask's test client.
    
    - setUpClass(cls): Set up the app and test client once for all tests

    === Testing User creation ===
        - test_01_create_user(self): Test successful user creation with UUID retrieval

    === Testing Place creation ===
        - test_02_create_place(self): Test successful place creation with valid user ID

    === Testing Review creation ===
        - test_03_create_review(self): Test successful review creation with valid request
        
    === Testing Place retrieval ===
        - test_04_get_all_places(self): Test retrieving all places
        - test_05_get_place_by_id(self): Test retrieving a place by its ID
        - test_06_update_place(self): Test updating an existing place
        
    === Testing Review retrieval and modification ===
        - test_07_get_all_reviews(self): Test retrieving all reviews
        - test_08_get_review_by_id(self): Test retrieving a review by its ID
        - test_09_update_review(self): Test updating an existing review
        - test_10_delete_review(self): Test deleting an existing review
    """

    @classmethod
    def setUpClass(cls):
        """Prépare l'application et le client de test une fois pour tous les tests."""
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_01_create_user(self):
        """Test de la création d'un utilisateur avec récupération de l'UUID."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })

        # Vérification du statut de la réponse
        self.assertEqual(response.status_code, 201)

        # Récupération de l'UUID de l'utilisateur créé
        message = json.loads(response.data)
        TestUserPlaceReviewEndpoints.user_id = message["id"]
        print("ID de l'utilisateur créé:", TestUserPlaceReviewEndpoints.user_id)

    def test_02_create_place(self):
        """Test de la création d'une place avec un utilisateur valide."""
        # S'assurer que le test précédent a créé un utilisateur
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'user_id'))

        # Création d'une place en utilisant l'UUID de l'utilisateur créé
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place in the city center",
            "price": 120.0,
            "latitude": 45.764043,
            "longitude": 4.835659,
            "owner_id": TestUserPlaceReviewEndpoints.user_id  # Utilisation de l'UUID récupéré
        })

        # Vérification du statut de la réponse
        self.assertEqual(response.status_code, 201)

        # Récupération de l'UUID de la place créée
        message = json.loads(response.data)
        TestUserPlaceReviewEndpoints.place_id = message["id"]
        print("ID de la place créée:", TestUserPlaceReviewEndpoints.place_id)

        # Vérification des données
        self.assertEqual(message["title"], "Cozy Apartment")
        self.assertEqual(message["owner_id"], TestUserPlaceReviewEndpoints.user_id)

    def test_03_create_review(self):
        """Test de la création d'un review pour la place créée par l'utilisateur."""
        # S'assurer que les tests précédents ont créé un utilisateur et une place
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'user_id'))
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'place_id'))

        # Création d'un review en utilisant l'UUID de l'utilisateur et de la place
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place, very cozy!",
            "rating": 5,
            "user_id": TestUserPlaceReviewEndpoints.user_id,
            "place_id": TestUserPlaceReviewEndpoints.place_id
        })

        # Vérification du statut de la réponse
        self.assertEqual(response.status_code, 201)

        # Récupération de l'UUID du review créé
        message = json.loads(response.data)
        TestUserPlaceReviewEndpoints.review_id = message["id"]
        print("ID du review créé:", TestUserPlaceReviewEndpoints.review_id)

        # Vérification des données
        self.assertEqual(message["text"], "Great place, very cozy!")
        self.assertEqual(message["rating"], 5)
        self.assertEqual(message["user_id"], TestUserPlaceReviewEndpoints.user_id)
        self.assertEqual(message["place_id"], TestUserPlaceReviewEndpoints.place_id)

    def test_04_get_all_places(self):
        """Test de la récupération de toutes les places."""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_05_get_place_by_id(self):
        """Test de la récupération d'une place par son ID."""
        # S'assurer qu'une place a été créée précédemment
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'place_id'))

        response = self.client.get(f'/api/v1/places/{TestUserPlaceReviewEndpoints.place_id}')
        self.assertEqual(response.status_code, 200)
        
        # Vérification du contenu de la place
        message = json.loads(response.data)
        self.assertEqual(message["title"], "Cozy Apartment")
        self.assertEqual(message["owner_id"], TestUserPlaceReviewEndpoints.user_id)

    def test_06_update_place(self):
        """Test de la mise à jour d'une place existante."""
        # S'assurer qu'une place a été créée précédemment
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'place_id'))

        updated_data = {
            "title": "Updated Apartment",
            "description": "A newly renovated place.",
            "price": 150.0,
            "latitude": 45.764043,
            "longitude": 4.835659,
            "owner_id": TestUserPlaceReviewEndpoints.user_id
        }
        
        response = self.client.put(
            f'/api/v1/places/{TestUserPlaceReviewEndpoints.place_id}', 
            json=updated_data
        )
        self.assertEqual(response.status_code, 200)
        
        # Vérification des données mises à jour
        message = json.loads(response.data)
        self.assertEqual(message["title"], "Updated Apartment")
        self.assertEqual(message["price"], 150.0)

    def test_07_get_all_reviews(self):
        """Test de la récupération de tous les reviews."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

    def test_08_get_review_by_id(self):
        """Test de la récupération d'un review par son ID."""
        # S'assurer qu'un review a été créé précédemment
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'review_id'))

        response = self.client.get(f'/api/v1/reviews/{TestUserPlaceReviewEndpoints.review_id}')
        self.assertEqual(response.status_code, 200)
        
        # Vérification du contenu du review
        message = json.loads(response.data)
        self.assertEqual(message["text"], "Great place, very cozy!")
        self.assertEqual(message["rating"], 5)

    def test_09_update_review(self):
        """Test de la mise à jour d'un review existant."""
        # S'assurer qu'un review a été créé précédemment
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'review_id'))

        updated_data = {
            "text": "Updated review text",
            "rating": 4,
            "user_id": TestUserPlaceReviewEndpoints.user_id,
            "place_id": TestUserPlaceReviewEndpoints.place_id
        }
        
        response = self.client.put(
            f'/api/v1/reviews/{TestUserPlaceReviewEndpoints.review_id}', 
            json=updated_data
        )
        self.assertEqual(response.status_code, 200)
        
        # Vérification des données mises à jour
        message = json.loads(response.data)
        self.assertEqual(message["text"], "Updated review text")
        self.assertEqual(message["rating"], 4)

    def test_10_delete_review(self):
        """Test de la suppression d'un review existant."""
        # S'assurer qu'un review a été créé précédemment
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'review_id'))

        response = self.client.delete(f'/api/v1/reviews/{TestUserPlaceReviewEndpoints.review_id}')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
