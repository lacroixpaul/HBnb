import unittest
from app.models.review import Review
from app.models.place import Place
from app.models.user import User


class TestReviewModel(unittest.TestCase):
    """
    Unit tests for the Review model.
    - setUp(self): set up a sample User, Place, and Review instance

    === Testing review creation ===
        - test_01_review_creation_success : valid request
        - test_02_review_creation_missing_text(self): missing text
        - test_03_review_creation_missing_author(self): missing author
        - test_04_review_creation_missing_place(self): missing place
        - test_05_review_creation_invalid_rating_negative : negative rating
        - test_06_review_creation_invalid_rating_exceed : > 5 rating

    === Testing to_dict method ===
        - test_07_to_dict_method(self): valid request
    """

    def setUp(self):
        """Set up a sample User, Place, and Review instance before each test."""
        # Create a test user
        self.test_user = User(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com"
        )
        self.user_id = self.test_user.id  # Retrieve the UUID

        # Create a test place using the generated user_id
        self.test_place = Place(
            title="Seaside Villa",
            price=300.0,
            latitude=34.052235,
            longitude=-118.243683,
            owner_id=self.user_id,
            description="A beautiful villa by the sea"
        )
        self.place_id = self.test_place.id  # Retrieve the UUID

        # Create a test review
        self.valid_review = Review(
            text="Amazing experience!",
            user_id=self.user_id,
            place_id=self.place_id,
            rating=5
        )

    def test_01_review_creation_success(self):
        """Test that a Review instance is correctly created with valid data."""
        self.assertEqual(self.valid_review.text, "Amazing experience!")
        self.assertEqual(self.valid_review.user_id, self.user_id)
        self.assertEqual(self.valid_review.place_id, self.place_id)

    def test_02_review_creation_missing_text(self):
        """Test that creating a Review without text raises a ValueError."""
        with self.assertRaises(ValueError):
            Review(
                text="",
                user_id=self.user_id,
                place_id=self.place_id,
                rating=5
            )

    def test_03_review_creation_missing_author(self):
        """Test that creating a Review without an author raises a ValueError."""
        with self.assertRaises(ValueError):
            Review(
                text="Nice place!",
                user_id=None,
                place_id=self.place_id,
                rating=5
            )

    def test_04_review_creation_missing_place(self):
        """Test that creating a Review without a place raises a ValueError."""
        with self.assertRaises(ValueError):
            Review(
                text="Nice view!",
                user_id=self.user_id,
                place_id=None,
                rating=5
            )

    def test_05_review_creation_invalid_rating_negative(self):
        """Test that creating a Review with a negative rating raises a ValueError."""
        with self.assertRaises(ValueError):
            Review(
                text="Terrible place!",
                user_id=self.user_id,
                place_id=self.place_id,
                rating=-1
            )

    def test_06_review_creation_invalid_rating_exceed(self):
        """Test that creating a Review with a rating > 5 raises a ValueError."""
        with self.assertRaises(ValueError):
            Review(
                text="Perfect place, but too good to be true!",
                user_id=self.user_id,
                place_id=self.place_id,
                rating=6
            )

    def test_07_to_dict_method(self):
        """Test that the to_dict method returns the correct dictionary representation."""
        review_dict = self.valid_review.to_dict()
        self.assertEqual(review_dict["text"], "Amazing experience!")
        self.assertEqual(review_dict["user_id"], self.user_id)
        self.assertEqual(review_dict["place_id"], self.place_id)
        self.assertIn("created_at", review_dict)
        self.assertIn("updated_at", review_dict)
        

if __name__ == "__main__":
    unittest.main()
