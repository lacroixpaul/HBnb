#!/usr/bin/python3
"""
Module review

This module defines the 'Review' class, which represents a user review for a place.
It inherits from BaseModel (defined in basemodel.py). 

The `Review` class includes the following attributes:
- text (str): The content of the review (required, non-empty string).
- rating (int): The rating given to the place (required, integer between 1 and 5).
- place (Place): The place associated with the review, represented as a `Place` instance (required).
- user (User): The user who wrote the review, represented as a `User` instance (required).
- ID : inherited from BaseModel.
- Date of creation / update : inherited from BaseModel.

Example usage:
    review = Review(
        text="Great place to stay! Highly recommended.",
        rating=5,
        place=place_instance,
        user=user_instance
    )
"""

from basemodel import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        """
        description
        """
        super().__init__()

        if not isinstance(text, str) or not text:
            raise ValueError("Content must be a string.")
        self.title = text
        
        if not isinstance(rating, int) or not rating or rating < 1 and rating > 5:
            raise ValueError("Rating must be an int between 1 and 5.")
        self.title = rating

        self.place = place # Need to be validated !!!
        self.user = user
