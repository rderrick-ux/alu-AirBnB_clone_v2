#!/usr/bin/python3
"""This module defines the Place class.

Place represents a rental property listing. It supports both
FileStorage (with property accessors) and DBStorage (with SQLAlchemy
relationships), including a Many-to-Many link with Amenity.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# This is the join table for the many-to-many relationship between
# Place and Amenity. It just holds pairs of (place_id, amenity_id).
# Example: place "Beach House" has amenities "Wifi" and "Pool"
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id', String(60),
        ForeignKey('places.id'),
        primary_key=True,
        nullable=False
    ),
    Column(
        'amenity_id', String(60),
        ForeignKey('amenities.id'),
        primary_key=True,
        nullable=False
    )
)


class Place(BaseModel, Base):
    """Represents a rental listing (like an Airbnb property)."""

    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        # DBStorage relationships
        # Deleting a place also deletes all its reviews
        reviews = relationship(
            'Review',
            backref='place',
            cascade='all, delete-orphan'
        )
        # Many-to-many with Amenity via the place_amenity table
        amenities = relationship(
            'Amenity',
            secondary='place_amenity',
            viewonly=False
        )
    else:
        # FileStorage: list of amenity ids linked to this place
        amenity_ids = []

        @property
        def reviews(self):
            """Return all Review objects for this place."""
            from models import storage
            from models.review import Review
            return [
                r for r in storage.all(Review).values()
                if r.place_id == self.id
            ]

        @property
        def amenities(self):
            """Return all Amenity objects linked to this place."""
            from models import storage
            from models.amenity import Amenity
            return [
                a for a in storage.all(Amenity).values()
                if a.id in self.amenity_ids
            ]

        @amenities.setter
        def amenities(self, obj):
            """Add an Amenity to this place by appending its id."""
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
