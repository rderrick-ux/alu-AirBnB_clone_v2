#!/usr/bin/python3
"""This module defines the User class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Represents a registered user of the application."""

    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)   # optional
    last_name = Column(String(128), nullable=True)    # optional

    # A user can own many places - deleting the user deletes their places
    places = relationship(
        'Place',
        backref='user',
        cascade='all, delete-orphan'
    )
    # A user can write many reviews - deleting the user deletes their reviews
    reviews = relationship(
        'Review',
        backref='user',
        cascade='all, delete-orphan'
    )
