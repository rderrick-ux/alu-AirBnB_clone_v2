#!/usr/bin/python3
"""This module defines the City class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Represents a city that belongs to a state (e.g. San Francisco)."""

    __tablename__ = 'cities'

    # Foreign key links each city to a row in the states table
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)

    # A city can have many places listed in it
    # Deleting a city also deletes all its places
    places = relationship(
        'Place',
        backref='cities',
        cascade='all, delete-orphan'
    )
