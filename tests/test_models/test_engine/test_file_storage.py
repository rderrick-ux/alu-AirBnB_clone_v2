#!/usr/bin/python3
"""Unit tests for the FileStorage class"""
import os
import unittest
from models.base_model import BaseModel
from models import storage
from models.state import State
from models.user import User


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') == 'db',
    'FileStorage tests only'
)
class TestFileStorage(unittest.TestCase):
    """Tests for the FileStorage class"""

    def setUp(self):
        """Clear storage before each test"""
        keys = list(storage.all().keys())
        for key in keys:
            del storage.all()[key]

    def tearDown(self):
        """Remove storage file after each test"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_obj_list_empty(self):
        """__objects is initially empty after setUp"""
        self.assertEqual(len(storage.all()), 0)

    def test_all_returns_dict(self):
        """all() returns a dict"""
        self.assertIsInstance(storage.all(), dict)

    def test_new(self):
        """new() adds object to __objects"""
        new = BaseModel()
        storage.new(new)
        key = 'BaseModel.' + new.id
        self.assertIn(key, storage.all())

    def test_all_with_class_filter(self):
        """all(cls) returns only objects of that class"""
        state = State()
        state.name = 'TestState'
        storage.new(state)
        result = storage.all(State)
        for obj in result.values():
            self.assertIsInstance(obj, State)

    def test_all_with_string_filter(self):
        """all('ClassName') filters correctly"""
        state = State()
        state.name = 'FilterTest'
        storage.new(state)
        result = storage.all('State')
        for obj in result.values():
            self.assertIsInstance(obj, State)

    def test_save(self):
        """save() creates the file"""
        new = BaseModel()
        storage.new(new)
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """reload() restores objects from file"""
        new = BaseModel()
        storage.new(new)
        storage.save()
        storage.reload()
        key = 'BaseModel.' + new.id
        self.assertIn(key, storage.all())

    def test_reload_from_nonexistent(self):
        """reload() does nothing when file does not exist"""
        self.assertIsNone(storage.reload())

    def test_reload_empty_file(self):
        """reload() raises ValueError on empty file"""
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_delete(self):
        """delete() removes object from __objects"""
        obj = BaseModel()
        storage.new(obj)
        key = 'BaseModel.' + obj.id
        self.assertIn(key, storage.all())
        storage.delete(obj)
        self.assertNotIn(key, storage.all())

    def test_delete_none(self):
        """delete(None) does nothing"""
        count_before = len(storage.all())
        storage.delete(None)
        self.assertEqual(len(storage.all()), count_before)

    def test_type_path(self):
        """__file_path is a string"""
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(FileStorage._FileStorage__file_path), str)

    def test_type_objects(self):
        """__objects is a dict"""
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """Keys follow ClassName.id format"""
        new = BaseModel()
        storage.new(new)
        self.assertIn('BaseModel.' + new.id, storage.all())

    def test_storage_var_created(self):
        """storage is a FileStorage instance"""
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)

    def test_base_model_instantiation(self):
        """File is not created on BaseModel instantiation alone"""
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_base_model_save(self):
        """BaseModel.save() calls storage save and creates file"""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))
