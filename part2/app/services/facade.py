from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        required_fields = ["first_name", "last_name", "email"]
        for field in required_fields:
            if field not in user_data or not user_data[field].strip():
                raise ValueError(f"Missing required field: {field}")

        if self.get_user_by_email(user_data['email']):
            raise ValueError("Email already registered")

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None

        user.update(user_data)
        return user

    def get_all_users(self):
        return self.user_repo.get_all()

    def create_place(self, place_data):
        required_fields = ["title", "price", "latitude", "longitude"]
        for field in required_fields:
            if field not in place_data or not place_data[field].strip():
                raise ValueError(f"Missing required field: {field}")
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("Owner ID is required.")
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError(f"No user found with the given owner ID: {owner_id}")
        place_data['owner'] = owner
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"No place found with ID: {place_id}")

        owner_id = place.owner
        owner = self.user_repo.get(owner_id)

        if not owner:
            raise ValueError("Owner not found for this place.")

        place.owner = owner
        amenities = self.amenity_repo.get_all()
        place.amenities = [amenity for amenity
                           in amenities if amenity.place_id == place_id]
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"No place found with ID: {place_id}")
        place.update(place_data)
        self.place_repo.add(place)
        return place

    def create_amenity(self, amenity_data):
        """Créer un équipement avec une vérification de doublon et validation des données"""
        new_name = amenity_data.get('name', "").strip()

        if not new_name:
            raise ValueError("Amenity name cannot be empty.")

        existing_amenities = self.get_all_amenities()
        for amenity in existing_amenities:
            if amenity.name.lower() == new_name.lower():
                raise ValueError("Amenity already exist.")

        amenity = Amenity(name=new_name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        new_name = amenity_data.get('name', "").strip()
        if not new_name:
            raise ValueError("Amenity name cannot be empty.")

        existing_amenities = self.get_all_amenities()
        for a in existing_amenities:
            if a.id != amenity_id and a.name.lower() == new_name.lower():
                raise ValueError(
                    "Another amenity with this name already exists.")

        amenity.name = new_name
        self.amenity_repo.add(amenity)  # Enregistrer la mise à jour
        return amenity

    def create_review(self, review_data):
        text = review_data.get('text', "").strip()
        rating = review_data.get('rating')
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        if not text:
            raise ValueError("Review text cannot be empty.")
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5.")
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found.")
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        review = Review(text=text, rating=rating, user=user, place=place)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found.")
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_all()
        place_reviews = [review for review in reviews if review.place.id == place_id]
        return place_reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"No review found with ID: {review_id}")
        text = review_data.get('text', "").strip()
        rating = review_data.get('rating')
        if text:
            review.text = text
        else:
            raise ValueError("Review text cannot be empty.")
        if isinstance(rating, int) and 1 <= rating <= 5:
            review.rating = rating
        elif rating is not None:
            raise ValueError("Rating must be an integer between 1 and 5.")
        self.review_repo.add(review)
        return review


    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"No review found with ID: {review_id}")
        self.review_repo.delete(review_id)
        return f"Review with ID {review_id} has been deleted."
