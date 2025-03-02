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
        - test_01c_create_user2(self): create User 2 for review testing
        - test_01d_user_cannot_modify_own_id(self): testing forbidding ID modification

    === Testing Place creation ===
        - test_02_create_place(self): Test successful place creation with valid user ID
        - test_02b_create_place_missing_attribute(self): Test invalid place creation 

    === Testing Review creation ===
        - test_03_create_review(self): Test successful review creation with valid request
        - test_03b_create_review_missing_attribute(self): Test invalid review creation
        - test_03c_create_review_owner(self): test reviewing own place

    === Testing Place retrieval ===
        - test_04_get_all_places(self): Test retrieving all places
        - test_05_get_place_by_id(self): Test retrieving a place by its ID
        - test_05b_get_place_by_invalid_id(self): Test retrieving a place by a wrong ID
        - test_06_update_place(self): Test updating an existing place
        - test_06b_update_place_invalid_id(self): Test invalid place update
        - test_06c_place_cannot_modify_own_id(self): testing forbidding ID modification

    === Testing Review retrieval and modification ===
        - test_07_get_all_reviews(self): Test retrieving all reviews
        - test_08_get_review_by_id(self): Test retrieving a review by its ID
        - test_09_update_review(self): Test updating an existing review
        - test_10_delete_review(self): Test deleting an existing review

    === Testing Amenity creation and modification === 
        - test_11_create_amenity(self): test successful amenity creation
        - test_12_create_duplicate_amenity(self): testing duplication protection
        - test_13_get_all_amenities(self): testing getting all amenity
        - test_14_update_amenity(self): testing updating amenity
        - test_15_update_nonexistent_amenity(self): testing updating non existing amenity

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

    def test_01c_create_user2(self):
        """Test successful creation of another user (user2)."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com"
        })
        self.assertEqual(response.status_code, 201)
        message = json.loads(response.data)
        TestUserPlaceReviewEndpoints.user2_id = message["id"]
        print("Created user2 ID:", TestUserPlaceReviewEndpoints.user2_id)

    def test_01d_user_cannot_modify_own_id(self):
        """Test that a user cannot modify their own 'id'."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'user_id'))
        response = self.client.put(f'/api/v1/users/{TestUserPlaceReviewEndpoints.user_id}', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "id": "new_invalid_id"
        })
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)
        self.assertIn("error", message)
        self.assertEqual(message["error"], "ID cannot be modified")

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
        self.assertEqual(message["owner_id"],
                         TestUserPlaceReviewEndpoints.user_id)

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
        self.assertEqual(
            message["message"], "Title must be a string of max. 100 characters.")

    def test_03_create_review(self):
        """Test successful review creation for the place created by the user."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'user2_id'))
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'place_id'))
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place, very cozy!",
            "rating": 5,
            "user_id": TestUserPlaceReviewEndpoints.user2_id,
            "place_id": TestUserPlaceReviewEndpoints.place_id
        })
        self.assertEqual(response.status_code, 201)
        message = json.loads(response.data)
        TestUserPlaceReviewEndpoints.review_id = message["id"]
        print("Created review ID:", TestUserPlaceReviewEndpoints.review_id)
        self.assertEqual(message["text"], "Great place, very cozy!")
        self.assertEqual(message["rating"], 5)
        self.assertEqual(message["user_id"],
                         TestUserPlaceReviewEndpoints.user2_id)
        self.assertEqual(message["place_id"],
                         TestUserPlaceReviewEndpoints.place_id)

    def test_03b_create_review_missing_attribute(self):
        """Test review creation with a missing attribute (no 'text')."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'user_id'))
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'place_id'))
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": TestUserPlaceReviewEndpoints.user2_id,
            "place_id": TestUserPlaceReviewEndpoints.place_id
        })
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)
        self.assertIn("message", message)
        self.assertEqual(message["message"], "Content must be a string.")

    def test_03c_create_review_owner(self):
        """Test owner cannot create a review for their own place."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'user_id'))
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'place_id'))
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Owner should not be able to review their own place.",
            "rating": 5,
            "user_id": TestUserPlaceReviewEndpoints.user_id,
            "place_id": TestUserPlaceReviewEndpoints.place_id
        })
        self.assertEqual(response.status_code, 403)
        message = json.loads(response.data)
        self.assertIn("message", message)
        self.assertEqual(message["message"],
                         "Owner cannot review their own place")

    def test_04_get_all_places(self):
        """Test retrieving all places."""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_05_get_place_by_id(self):
        """Test retrieving a place by its ID."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'place_id'))
        response = self.client.get(
            f'/api/v1/places/{TestUserPlaceReviewEndpoints.place_id}')
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data)
        self.assertEqual(message["title"], "Cozy Apartment")
        self.assertEqual(message["owner_id"],
                         TestUserPlaceReviewEndpoints.user_id)

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
        response = self.client.put(
            '/api/v1/places/invalid-id', json=updated_data)
        self.assertEqual(response.status_code, 404)
        message = json.loads(response.data)
        self.assertIn("message", message)

    def test_06c_place_cannot_modify_own_id(self):
        """Test that a place's ID cannot be modified."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'place_id'))
        updated_data = {
            "id": "new-id",
            "title": "Updated Apartment",
            "description": "A newly renovated place.",
            "price": 150.0,
            "latitude": 45.764043,
            "longitude": 4.835659,
            "owner_id": TestUserPlaceReviewEndpoints.user2_id
        }
        response = self.client.put(
            f'/api/v1/places/{TestUserPlaceReviewEndpoints.place_id}',
            json=updated_data
        )
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)
        self.assertIn("error", message)
        self.assertEqual(message["error"], "Place ID cannot be modified")

    def test_07_get_all_reviews(self):
        """Test retrieving all reviews."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

    def test_08_get_review_by_id(self):
        """Test retrieving a review by its ID."""
        self.assertTrue(hasattr(TestUserPlaceReviewEndpoints, 'review_id'))
        response = self.client.get(
            f'/api/v1/reviews/{TestUserPlaceReviewEndpoints.review_id}')
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
        response = self.client.delete(
            f'/api/v1/reviews/{TestUserPlaceReviewEndpoints.review_id}')
        self.assertEqual(response.status_code, 200)

    def test_11_create_amenity(self):
        """Test the creation of an Amenity"""
        response = self.client.post(
            "/api/v1/amenities/", json={"name": "WiFi"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["name"], "WiFi")

    def test_12_create_duplicate_amenity(self):
        """Test that creating a duplicate Amenity fails"""
        response = self.client.post(
            "/api/v1/amenities/", json={"name": "WiFi"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_13_get_all_amenities(self):
        """Test retrieving all amenities"""
        self.client.post("/api/v1/amenities/", json={"name": "Pool"})
        response = self.client.get("/api/v1/amenities/")
        self.assertEqual(response.status_code, 200)
        amenities = response.json
        self.assertIsInstance(amenities, list)
        self.assertGreaterEqual(len(amenities), 2)
        amenity_names = [a["name"] for a in amenities]
        self.assertIn("WiFi", amenity_names)
        self.assertIn("Pool", amenity_names)

    def test_14_update_amenity(self):
        """Test updating an existing amenity."""
        response = self.client.post("/api/v1/amenities/", json={"name": "Gym"})
        self.assertEqual(response.status_code, 201)
        amenity_id = response.json["id"]
        updated_data = {"name": "Sport Gym"}
        response = self.client.put(
            f"/api/v1/amenities/{amenity_id}", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Sport Gym")

    def test_15_update_nonexistent_amenity(self):
        """Test updating a non-existent amenity"""
        response = self.client.put(
            "/api/v1/amenities/123e4567-e89b-12d3-a456-426614174000",
            json={"name": "New Name"}
        )
        print("Response data:", response.json)  # Debug

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "Amenity not found")


if __name__ == '__main__':
    unittest.main()
