from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
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
        price = place_data.get('price')
        if not isinstance(price, (float, int)) or price < 0:
            raise ValueError("Price must be a positive number.")

        latitude = place_data.get('latitude')
        if not isinstance(latitude, (float,
                                     int)) or not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be a float between -90.0 and 90.0")

        longitude = place_data.get('longitude')
        if not isinstance(longitude, (float, int)) or not \
                (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be a float \
                between -180.0 and 180.0.")

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
        # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        pass

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        pass

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        pass

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        pass

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        pass
