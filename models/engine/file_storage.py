#!/usr/bin/python3
"""This module defines FileStorage - stores objects as JSON on disk.

FileStorage is the default storage engine used when HBNB_TYPE_STORAGE
is not set to 'db'. All data is kept in a local file.json file.
"""
import json


class FileStorage:
    """Saves and loads all model objects to/from a JSON file.

    Objects are kept in memory in __objects (a plain dictionary).
    When save() is called they are written to file.json.
    When reload() is called they are read back from file.json.
    """

    __file_path = 'file.json'   # where data is stored on disk
    __objects = {}              # all objects live here while the app runs

    def all(self, cls=None):
        """Return the dictionary of stored objects.

        If cls is given, only return objects of that class.
        cls can be the class itself or just its name as a string.
        """
        if cls is None:
            return FileStorage.__objects

        result = {}
        for key, obj in FileStorage.__objects.items():
            if isinstance(cls, str):
                # cls was passed as a string like 'State'
                if type(obj).__name__ == cls:
                    result[key] = obj
            else:
                # cls was passed as the actual class like State
                if isinstance(obj, cls):
                    result[key] = obj
        return result

    def new(self, obj):
        """Add obj to __objects using key format 'ClassName.id'."""
        key = '{}.{}'.format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Convert all objects to dicts and write them to file.json."""
        temp = {}
        for key, val in FileStorage.__objects.items():
            temp[key] = val.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        """Read file.json and recreate all the objects stored there."""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        # Map class names (strings) to the actual classes
        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
            for key, val in temp.items():
                cls_name = val.get('__class__')
                if cls_name in classes:
                    # Recreate the object by passing the dict as kwargs
                    FileStorage.__objects[key] = classes[cls_name](**val)
        except FileNotFoundError:
            # No file yet - that's fine, just start with an empty storage
            pass

    def delete(self, obj=None):
        """Remove obj from __objects. Does nothing if obj is None."""
        if obj is None:
            return
        key = '{}.{}'.format(type(obj).__name__, obj.id)
        FileStorage.__objects.pop(key, None)

    def close(self):
        """Reload from disk - used to refresh data between requests."""
        self.reload()
