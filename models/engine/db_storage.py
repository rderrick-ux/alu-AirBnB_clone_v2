#!/usr/bin/python3
"""This module defines DBStorage - stores objects in a MySQL database.

DBStorage is activated when HBNB_TYPE_STORAGE=db. It uses SQLAlchemy
to manage a MySQL session and persist all model objects to the database.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Saves and loads model objects to/from a MySQL database.

    Uses SQLAlchemy, which lets us work with database rows as Python objects
    instead of writing raw SQL queries.

    A 'session' is like a temporary workspace: you make changes in the
    session and then commit() to actually save them to the database.
    """

    __engine = None   # the connection to the database
    __session = None  # the current workspace for reading/writing rows

    def __init__(self):
        """Connect to the MySQL database using environment variables."""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        db = os.getenv('HBNB_MYSQL_DB')

        # Build the connection string and create the engine
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db),
            pool_pre_ping=True  # test connection before using it
        )

        # In test mode, wipe all tables so each test run starts clean
        if os.getenv('HBNB_ENV') == 'test':
            from models.base_model import Base
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects from the database.

        Returns a dict like {'State.abc123': <State object>, ...}.
        If cls is given, only return objects of that class.
        """
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
            'User': User, 'State': State, 'City': City,
            'Amenity': Amenity, 'Place': Place, 'Review': Review
        }

        result = {}
        if cls is not None:
            # Convert string class name to actual class if needed
            if isinstance(cls, str):
                cls = classes.get(cls)
            if cls is not None:
                for obj in self.__session.query(cls).all():
                    key = '{}.{}'.format(type(obj).__name__, obj.id)
                    result[key] = obj
        else:
            # No filter - query every model class
            for c in classes.values():
                for obj in self.__session.query(c).all():
                    key = '{}.{}'.format(type(obj).__name__, obj.id)
                    result[key] = obj
        return result

    def new(self, obj):
        """Stage obj so it will be saved on the next commit."""
        self.__session.add(obj)

    def save(self):
        """Commit all staged changes - this actually writes to the DB."""
        self.__session.commit()

    def delete(self, obj=None):
        """Mark obj for deletion. Call save() after to apply it."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the DB and open a new session."""
        from models.base_model import Base
        # Import all models so SQLAlchemy knows about their tables
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        # Create any tables that don't exist yet
        Base.metadata.create_all(self.__engine)

        # scoped_session makes the session thread-safe
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the session when we're done."""
        self.__session.close()
