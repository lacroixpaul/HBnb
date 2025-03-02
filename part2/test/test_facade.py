#!/usr/bin/python3
import unittest
from app.services.facade import HBnBFacade
from app.models.place import Place
from app.models.user import User
from app.models.review import Review


class TestHBnBFacade(unittest.TestCase):
    def setUp(self):
        """
        This method runs before each test.
        It initializes an instance of the facade for each test case.
        """
        self.facade = HBnBFacade()

    # Test create_place
    def test_create_place_success(self):
        """
        Test the create_place function with valid data.
        """
        place_data = {
            'title': "Charming Beach House",
            'price': 150.0,
            'latitude': 34.0194,
            'longitude': -118.4912,
            'owner_id': self.user.id,
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
            'owner_id': self.user.id,
            'description': "Beautiful view of the ocean."
        }
        with self.assertRaises(ValueError):
            self.facade.create_place(place_data)

    def test_create_place_invalid_latitude(self):
        """
        Test create_place with an invalid latitude.
        """
        place_data = {
            'title': "Charming Beach House",
            'price': 150.0,
            'latitude': -91.0,  # Invalid latitude
            'longitude': -118.4912,
            'owner_id': self.user.id,
            'description': "Beautiful view of the ocean."
        }
        with self.assertRaises(ValueError):
            self.facade.create_place(place_data)

    def test_create_place_invalid_owner(self):
        """
        Test create_place with an invalid owner (missing ID).
        """
        place_data = {
            'title': "Charming Beach House",
            'price': 150.0,
            'latitude': 34.0194,
            'longitude': -118.4912,
            'owner_id': None,
            'description': "Beautiful view of the ocean."
        }
        with self.assertRaises(ValueError):
            self.facade.create_place(place_data)

    def test_get_place_not_found(self):
        """
        Test get_place with a non-existent ID.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    """
        with self.assertRaises(ValueError):
            self.facade.get_place("invalid_id")

    def test_get_place_empty_id(self):
        """
        Test get_place with an empty ID.
        """
        with self.assertRaises(ValueError):
            self.facade.get_place("")

    # Test get_all_places
    def b_test_get_all_places(self):
        """
        Test get_all_places to check if all places are returned.
        """
        place1 = {
            'title': "City Apartment",
            'price': 200.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': self.user.id,
            'description': "Modern apartment in the city center."
        }
        place2 = {
            'title': "Countryside Villa",
            'price': 300.0,
            'latitude': 51.5074,
            'longitude': -0.1278,
            'owner_id': self.user.id,
            'description': "Spacious villa in the countryside."
        }
        self.facade.create_place(place1)
        self.facade.create_place(place2)

        places = self.facade.get_all_places()
        self.assertEqual(len(places), 2)

    def a_test_get_all_places_empty(self):
        """
        Test get_all_places with no places added.
        """
        # Now check if no places are returned
        places = self.facade.get_all_places()
        self.assertEqual(len(places), 0)

    def test_get_all_places_invalid_data(self):
        """
        Test get_all_places with corrupted data in the repository.
        """
        place_data = {
            'title': "Corrupted Place",
            'price': "invalid",  # Invalid price
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': self.user.id,
            'description': "This place has corrupted data."
        }
        with self.assertRaises(ValueError):
            self.facade.create_place(place_data)

    # Test update_place
    def test_update_place_success(self):
        """
        Test update_place with valid data.
        """
        place_data = {
            'title': "Old Title",
            'price': 120.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': self.user.id,
            'description': "An old description."
        }
        place = self.facade.create_place(place_data)
        update_data = {
            'title': "New Title",
            'description': "A brand new description"
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


# Test Review Functionality in HBnBFacade

    def setUp(self):
        """
        This method runs before each test.
        It initializes an instance of the facade for each test case.
        It also sets up a user and a place since reviews depend on them.
        """
        self.facade = HBnBFacade()
        # Creating a user
        self.user_data = {
            'first_name': "Review",
            'last_name': "Tester",
            'email': "review.tester@example.com"
        }
        self.user = self.facade.create_user(self.user_data)

        # Creating a place
        self.place_data = {
            'title': "Test Place",
            'price': 100.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': self.user.id,
            'description': "Test Description"
        }
        self.place = self.facade.create_place(self.place_data)

    # Test create_review
    def test_create_review_success(self):
        """
        Test creating a review with valid data.
        """
        review_data = {
            'text': "Great place!",
            'rating': 5,
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        review = self.facade.create_review(review_data)
        self.assertIsInstance(review, Review)
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)

    def test_create_review_empty_text(self):
        """
        Test creating a review with empty text.
        """
        review_data = {
            'text': "",
            'rating': 5,
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        with self.assertRaises(ValueError):
            self.facade.create_review(review_data)

    def test_create_review_invalid_rating(self):
        """
        Test creating a review with an invalid rating.
        """
        review_data = {
            'text': "Nice place",
            'rating': 6,  # Invalid rating
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        with self.assertRaises(ValueError):
            self.facade.create_review(review_data)

    def test_create_review_user_not_found(self):
        """
        Test creating a review with a non-existent user.
        """
        review_data = {
            'text': "Nice place",
            'rating': 4,
            'user_id': "nonexistent_user",
            'place_id': self.place.id
        }
        with self.assertRaises(ValueError):
            self.facade.create_review(review_data)

    def test_create_review_place_not_found(self):
        """
        Test creating a review with a non-existent place.
        """
        review_data = {
            'text': "Nice place",
            'rating': 4,
            'user_id': self.user.id,
            'place_id': "nonexistent_place"
        }
        with self.assertRaises(ValueError):
            self.facade.create_review(review_data)

    # Test get_review
    def test_get_review_success(self):
        """
        Test retrieving a review by its ID.
        """
        review_data = {
            'text': "Amazing stay!",
            'rating': 5,
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        review = self.facade.create_review(review_data)
        fetched_review = self.facade.get_review(review.id)
        self.assertEqual(fetched_review.text, "Amazing stay!")
        self.assertEqual(fetched_review.rating, 5)

    def test_get_review_not_found(self):
        """
        Test get_review with a non-existent ID.
        """
        with self.assertRaises(ValueError):
            self.facade.get_review("nonexistent_review")

    # Test get_all_reviews
    def test_get_all_reviews(self):
        """
        Test get_all_reviews to check if all reviews are returned.
        """
        review_data1 = {
            'text': "Nice place",
            'rating': 4,
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        review_data2 = {
            'text': "Not bad",
            'rating': 3,
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        self.facade.create_review(review_data1)
        self.facade.create_review(review_data2)

        reviews = self.facade.get_all_reviews()
        self.assertEqual(len(reviews), 2)

    # Test get_reviews_by_place
    def test_get_reviews_by_place(self):
        """
        Test getting reviews by place ID.
        """
        review_data = {
            'text': "Loved it!",
            'rating': 5,
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        self.facade.create_review(review_data)

        reviews = self.facade.get_reviews_by_place(self.place.id)
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0].text, "Loved it!")

    # Test update_review
    def test_update_review_success(self):
        """
        Test updating a review with valid data.
        """
        review_data = {
            'text': "Good place",
            'rating': 4,
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        review = self.facade.create_review(review_data)
        update_data = {
            'text': "Excellent place",
            'rating': 5
        }
        updated_review = self.facade.update_review(review.id, update_data)
        self.assertEqual(updated_review.text, "Excellent place")
        self.assertEqual(updated_review.rating, 5)

    def test_update_review_not_found(self):
        """
        Test update_review with a non-existent ID.
        """
        with self.assertRaises(ValueError):
            self.facade.update_review(
                "nonexistent_review", {'text': "Updated"})

    # Test delete_review
    def test_delete_review_success(self):
        """
        Test deleting a review.
        """
        review_data = {
            'text': "To be deleted",
            'rating': 3,
            'user_id': self.user.id,
            'place_id': self.place.id
        }
        review = self.facade.create_review(review_data)
        result = self.facade.delete_review(review.id)
        self.assertEqual(
            result, f"Review with ID {review.id} has been deleted.")
        with self.assertRaises(ValueError):
            self.facade.get_review(review.id)

    def test_delete_review_not_found(self):
        """
        Test delete_review with a non-existent ID.
        """
        with self.assertRaises(ValueError):
            self.facade.delete_review("nonexistent_review")


if __name__ == '__main__':
    unittest.main()
