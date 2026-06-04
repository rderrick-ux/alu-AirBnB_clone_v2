#!/usr/bin/python3
"""This module defines the State class."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Represents a US state (e.g. California).

    Inherits from both BaseModel (id, timestamps, save, etc.)
    and Base (so SQLAlchemy can map it to the 'states' table).
    """

    __tablename__ = 'states'  # name of the table in the database

    # The state's name, e.g. "California" - required, max 128 chars
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        # DBStorage: SQLAlchemy relationship - State.cities gives all cities
        # cascade='all, delete-orphan' means deleting a state also deletes
        # all its cities automatically
        cities = relationship(
            'City',
            backref='state',
            cascade='all, delete-orphan'
        )
    else:
        # FileStorage: manually filter cities that belong to this state
        @property
        def cities(self):
            """Return all City objects whose state_id matches this state."""
            from models import storage
            from models.city import City
            return [
                c for c in storage.all(City).values()
                if c.state_id == self.id
            ]
