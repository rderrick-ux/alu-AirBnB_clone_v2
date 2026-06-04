#!/usr/bin/python3
"""This module instantiates the appropriate storage object.

We check the environment variable HBNB_TYPE_STORAGE:
  - If it equals 'db'  -> use MySQL via SQLAlchemy (DBStorage)
  - Otherwise          -> use a JSON file (FileStorage)

This lets us switch storage engines without changing any model code.
"""
import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Load any existing data into memory
storage.reload()
