#!/usr/bin/python3
"""This module defines the Amenity class."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Represents a feature a place can offer (e.g. Wifi, Pool)."""

    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = relationship(
            'Place',
            secondary='place_amenity',
            viewonly=False
        )
