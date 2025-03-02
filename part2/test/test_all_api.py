import unittest
import json
from app import create_app


class TestUserPlaceReviewEndpoints(unittest.TestCase):
    """
    Unit tests for User, Place, and Review endpoints using Flask's test client.
    
    - setUpClass(cls): Set up the app and test client once for all tests

    === Testing User creation ===
        - test_01_create_user(self): Test successful user creation with UUID retrieval
        - test_01b_create_invalid_user(self): Test invalid user creation 

    === Testing Place creation ===
        - test_02_create_place(self): Test successful place creation with valid user ID
        - test_02b_create_place_missing_attribute(self):  Test invalid place creation 

    === Testing Review creation ===
        - test_03_create_review(self): Test successful review creation with valid request
        - test_03b_create_review_missing_attribute(self): Test invalid review creation
        
    === Testing Place retrieval ===
        - test_04_get_all_places(self): Test retrieving all places
        - test_05_get_place_by_id(self): Test retrieving a place by its ID
        - test_05b_get_place_by_invalid_id(self): Test retrieving a place by a wrong ID
        - test_06_update_place(self): Test updating an existing place
        - test_06b_update_place_invalid_id(self): Test invalid place update 
        
    === Testing Review retrieval and modification ===
        - test_07_get_all_reviews(self): Test retrieving all reviews
        - test_08_get_review_by_id(self): Test retrieving a review by its ID
        - test_09_update_review(self): Test updating an existing review
        - test_10_delete_review(self): Test deleting an existing review
    """

    @classmethod
    def setUpClass(cls):
        """Sets up the app and test client once for all tests."""
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_01_create_user(self):
        """Test successful user creation with UUID retrieval."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })

        self.assertEqual(response.status_code, 201)
        message = json.loads(response.data)
        TestUserPlaceReviewEndpoints.user_id = message["id"]
        print("Created user ID:", TestUserPlaceReviewEndpoints.user_id)

    def test_01b_create_invalid_user(self):
        """Test invalid user creation (missing fields)."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)
        self.assertIn("error", message)

    def test_02_create_place(self):
        """Test successful place creation with valid user ID."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'user_id'))
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place in the city center",
            "price": 120.0,
            "latitude": 45.764043,
            "longitude": 4.835659,
            "owner_id": TestUserPlaceReviewEndpoints.user_id
        })
        self.assertEqual(response.status_code, 201)
        message = json.loads(response.data)
        TestUserPlaceReviewEndpoints.place_id = message["id"]
        print("Created place ID:", TestUserPlaceReviewEndpoints.place_id)
        self.assertEqual(message["title"], "Cozy Apartment")
        self.assertEqual(message["owner_id"], TestUserPlaceReviewEndpoints.user_id)

    def test_02b_create_place_missing_attribute(self):
        """Test place creation with a missing attribute (no 'title')."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'user_id'))

        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "A nice place in the city center",
            "price": 120.0,
            "latitude": 45.764043,
            "longitude": 4.835659,
            "owner_id": TestUserPlaceReviewEndpoints.user_id
        })
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)
        self.assertIn("message", message)
        self.assertEqual(message["message"], "Title must be a string of max. 100 characters.")

    def test_03_create_review(self):
        """Test successful review creation for the place created by the user."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'user_id'))
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'place_id'))
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place, very cozy!",
            "rating": 5,
            "user_id": TestUserPlaceReviewEndpoints.user_id,
            "place_id": TestUserPlaceReviewEndpoints.place_id
        })
        self.assertEqual(response.status_code, 201)
        message = json.loads(response.data)
        TestUserPlaceReviewEndpoints.review_id = message["id"]
        print("Created review ID:", TestUserPlaceReviewEndpoints.review_id)
        self.assertEqual(message["text"], "Great place, very cozy!")
        self.assertEqual(message["rating"], 5)
        self.assertEqual(message["user_id"], TestUserPlaceReviewEndpoints.user_id)
        self.assertEqual(message["place_id"], TestUserPlaceReviewEndpoints.place_id)

    def test_03b_create_review_missing_attribute(self):
        """Test review creation with a missing attribute (no 'text')."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'user_id'))
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'place_id'))
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": TestUserPlaceReviewEndpoints.user_id,
            "place_id": TestUserPlaceReviewEndpoints.place_id
        })
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)
        self.assertIn("message", message)
        self.assertEqual(message["message"], "Content must be a string.")

    def test_04_get_all_places(self):
        """Test retrieving all places."""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_05_get_place_by_id(self):
        """Test retrieving a place by its ID."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'place_id'))
        response = self.client.get(f'/api/v1/places/{TestUserPlaceReviewEndpoints.place_id}')
        self.assertEqual(response.status_code, 200)        
        message = json.loads(response.data)
        self.assertEqual(message["title"], "Cozy Apartment")
        self.assertEqual(message["owner_id"], TestUserPlaceReviewEndpoints.user_id)

    def test_05b_get_place_by_invalid_id(self):
        """Test retrieving a place by an invalid ID."""
        response = self.client.get('/api/v1/places/invalid-id')
        self.assertEqual(response.status_code, 404)
        message = json.loads(response.data)
        self.assertIn("message", message)

    def test_06_update_place(self):
        """Test updating an existing place."""
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
        message = json.loads(response.data)
        self.assertEqual(message["title"], "Updated Apartment")
        self.assertEqual(message["price"], 150.0)

    def test_06b_update_place_invalid_id(self):
        """Test updating a place with an invalid ID."""
        updated_data = {
            "title": "Updated Apartment",
            "description": "A newly renovated place.",
            "price": 150.0,
            "latitude": 45.764043,
            "longitude": 4.835659,
            "owner_id": TestUserPlaceReviewEndpoints.user_id
        }
        response = self.client.put('/api/v1/places/invalid-id', json=updated_data)
        self.assertEqual(response.status_code, 404)
        message = json.loads(response.data)
        self.assertIn("message", message)

    def test_07_get_all_reviews(self):
        """Test retrieving all reviews."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

    def test_08_get_review_by_id(self):
        """Test retrieving a review by its ID."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'review_id'))
        response = self.client.get(f'/api/v1/reviews/{TestUserPlaceReviewEndpoints.review_id}')
        self.assertEqual(response.status_code, 200)        
        message = json.loads(response.data)
        self.assertEqual(message["text"], "Great place, very cozy!")
        self.assertEqual(message["rating"], 5)

    def test_09_update_review(self):
        """Test updating an existing review."""
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
        message = json.loads(response.data)
        self.assertEqual(message["text"], "Updated review text")
        self.assertEqual(message["rating"], 4)

    def test_10_delete_review(self):
        """Test deleting an existing review."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'review_id'))
        response = self.client.delete(f'/api/v1/reviews/{TestUserPlaceReviewEndpoints.review_id}')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
