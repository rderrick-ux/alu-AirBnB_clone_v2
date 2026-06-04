#!/usr/bin/python3
"""Unit tests for the Amenity class"""
import os
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):
    """Tests for the Amenity class"""

    def test_is_subclass(self):
        """Amenity inherits from BaseModel"""
        a = Amenity()
        self.assertIsInstance(a, BaseModel)

    def test_instantiation(self):
        """Amenity can be instantiated"""
        a = Amenity()
        self.assertIsNotNone(a.id)

    def test_to_dict_no_sa_state(self):
        """to_dict does not contain _sa_instance_state"""
        a = Amenity()
        a.name = 'Pool'
        d = a.to_dict()
        self.assertNotIn('_sa_instance_state', d)
        self.assertEqual(d['__class__'], 'Amenity')

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage attribute test only'
    )
    def test_name_class_attribute(self):
        """name is a class attribute"""
        self.assertIn('name', Amenity.__dict__)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage tests only'
    )
    def test_save(self):
        """save() works and updates updated_at"""
        from models import storage
        a = Amenity()
        a.name = 'Wifi'
        a.save()
        self.assertIsNotNone(a.updated_at)
        storage.delete(a)
        storage.save()
