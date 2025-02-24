#!/usr/bin/python3
"""

Module place

This module defines the 'Place' class, which define a rental place.
It inherit from BaseModel (defined in basemodel.py).

The `Place` class includes the following attributes:
- title (str): The title of the place (required, max 100 characters).
- price (float): Price per night for the place (required, must be positive).
- latitude (float): Latitude coordinate for the place's location
    (required, between -90.0 and 90.0).
- longitude (float): Longitude coordinate for the place's location
    (required, between -180.0 and 180.0).
- owner (User): The owner of the place, represented
    as a `User` instance (required).
- description (str): Detailed description of the place (optional).
- ID : inherited from BaseModel.
- Date of creation / update : inherited from BaseModel.

Example usage:
    place = Place(
        title="Fancy Citytown appartment",
        price=100.0,
        latitude=44.854034800092016,
        longitude=-0.5378175356439316,
        owner=user_instance,
        description="Convenient flat for work travel."
    )

"""

from .basemodel import BaseModel


class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude,
                 owner, description=None):
        """
        Create a new place
        """
        super().__init__()

        if not isinstance(title, str) or not title or len(title) > 100:
            raise ValueError("Title must be a string of max. 100 characters.")
        self.title = title

        if owner is None or not hasattr(owner, 'id'):
            raise ValueError("Owner is required and must \
                be a valid User instance.")

        self.owner = owner
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

        if description is not None and not isinstance(description, str):
            raise TypeError("Description must be a string.")
        self.description = description

        self.reviews = []
        self.amenities = []

    @property
    def price(self):
        return (self.__price)

    @price.setter
    def price(self, value):
        if not isinstance(value, (float, int)) or value < 0:
            raise ValueError("Price must be a positive number.")
        self.__price = float(value)

    @property
    def latitude(self):
        return (self.__latitude)

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (float, int)) or not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be a float between -90.0 and 90.0")
        self.__latitude = float(value)

    @property
    def longitude(self):
        return (self.__latitude)

    @latitude.setter
    def longitude(self, value):
        if not isinstance(value, (float, int)) or not \
                (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be a float \
                between -180.0 and 180.0.")
        self._longitude = float(value)

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self):
        """Converts the place instance to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
