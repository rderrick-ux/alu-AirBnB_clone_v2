#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Base is the foundation SQLAlchemy needs to map our classes to DB tables.
# Every model that should be saved to the database must inherit from Base.
Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models.

    All other classes (User, State, City, etc.) inherit from this class
    so they all share the same id, created_at, and updated_at fields.
    """

    # These three columns exist in every table in the database
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Create a new instance.

        If kwargs is given (e.g. loaded from file), use those values.
        Otherwise generate a fresh id and timestamps.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    # Skip the class name - we don't store it as an attribute
                    continue
                # Convert date strings back to datetime objects
                if key in ('created_at', 'updated_at'):
                    if isinstance(value, str):
                        value = datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%S.%f'
                        )
                setattr(self, key, value)
            # Fill in any missing fields
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.utcnow()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            # Brand new object - generate everything fresh
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """Return a readable string like: [ClassName] (id) {attributes}"""
        # _sa_instance_state is added by SQLAlchemy internally - we hide it
        d = {k: v for k, v in self.__dict__.items()
             if k != '_sa_instance_state'}
        return '[{}] ({}) {}'.format(type(self).__name__, self.id, d)

    def save(self):
        """Stamp the current time on updated_at and write to storage."""
        from models import storage
        self.updated_at = datetime.utcnow()
        # Register this object with storage, then persist it
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a plain dictionary of all attributes.

        This is used when saving to JSON or returning data.
        Dates are converted to ISO strings so they can be serialized.
        """
        dictionary = self.__dict__.copy()
        # Add the class name so we know which class to recreate later
        dictionary['__class__'] = type(self).__name__
        # Convert datetime objects to strings
        if isinstance(dictionary.get('created_at'), datetime):
            dictionary['created_at'] = dictionary['created_at'].isoformat()
        if isinstance(dictionary.get('updated_at'), datetime):
            dictionary['updated_at'] = dictionary['updated_at'].isoformat()
        # Remove SQLAlchemy's internal tracking key - not needed outside ORM
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def delete(self):
        """Remove this instance from storage."""
        from models import storage
        storage.delete(self)
