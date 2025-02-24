#!/usr/bin/python3
"""
Module amenity

This module defines the 'Amenity' class, which represents an amenity that can be associated with a place.
It inherits from BaseModel (defined in basemodel.py).

The `Amenity` class includes the following attributes:
- name (str): The name of the amenity (required, non-empty string with a maximum length of 50).
- ID: Inherited from BaseModel.
- Date of creation / update: Inherited from BaseModel.

Example usage:
    amenity = Amenity(name="Wi-Fi")
"""

import re
from .basemodel import BaseModel


class Amenity(BaseModel):
    """Represents a Amenity with validation for name."""

    def __init__(self, name):
        super().__init__()  # Initialize BaseModel (UUID, created_at, updated_at)
        self.name = self.validate_name(name)

    def validate_name(self, name):
        """Validates that the name is a string with a maximum length of 50."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        if len(name) > 50:
            raise ValueError("Name cannot exceed 50 characters.")
        return name

    def to_dict(self):
        """Converts the user instance to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
