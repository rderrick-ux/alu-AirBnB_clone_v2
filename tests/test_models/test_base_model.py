#!/usr/bin/python3
"""Unit tests for the BaseModel class"""
import os
import unittest
import datetime
from uuid import UUID
import json
from models.base_model import BaseModel


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') == 'db',
    'FileStorage tests only'
)
class TestBaseModel(unittest.TestCase):
    """Tests for BaseModel with FileStorage"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def tearDown(self):
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_default(self):
        """Test default instantiation"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Test instantiation from kwargs does not return same object"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Test that integer key in kwargs raises TypeError"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_kwargs_one(self):
        """Test partial kwargs sets attribute and generates missing fields"""
        n = {'Name': 'test'}
        new = self.value(**n)
        self.assertEqual(new.Name, 'test')
        self.assertIsNotNone(new.id)
        self.assertIsInstance(new.created_at, datetime.datetime)

    def test_save(self):
        """Test that save persists instance to file"""
        i = self.value()
        i.save()
        key = self.name + '.' + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """Test string representation format"""
        i = self.value()
        d = {k: v for k, v in i.__dict__.items()
             if k != '_sa_instance_state'}
        self.assertEqual(
            str(i), '[{}] ({}) {}'.format(self.name, i.id, d)
        )

    def test_todict(self):
        """Test to_dict returns correct dictionary"""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """Test that None key in kwargs raises TypeError"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_id(self):
        """Test id is a string"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_id_is_uuid(self):
        """Test id is a valid UUID"""
        new = self.value()
        try:
            UUID(new.id)
            valid = True
        except ValueError:
            valid = False
        self.assertTrue(valid)

    def test_created_at(self):
        """Test created_at is a datetime"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """Test updated_at is a datetime"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertIsInstance(new.updated_at, datetime.datetime)

    def test_to_dict_has_class_key(self):
        """Test to_dict includes __class__ key"""
        i = self.value()
        d = i.to_dict()
        self.assertIn('__class__', d)
        self.assertEqual(d['__class__'], self.name)

    def test_to_dict_no_sa_state(self):
        """Test to_dict does not include _sa_instance_state"""
        i = self.value()
        d = i.to_dict()
        self.assertNotIn('_sa_instance_state', d)

    def test_two_instances_have_different_ids(self):
        """Test two BaseModel instances have different ids"""
        a = self.value()
        b = self.value()
        self.assertNotEqual(a.id, b.id)

    def test_delete(self):
        """Test delete removes instance from storage"""
        from models import storage
        i = self.value()
        i.save()
        key = '{}.{}'.format(self.name, i.id)
        self.assertIn(key, storage.all())
        i.delete()
        self.assertNotIn(key, storage.all())
