#!/usr/bin/python3
"""Unit tests for the City class"""
import os
import unittest
from models.city import City
from models.base_model import BaseModel


class TestCity(unittest.TestCase):
    """Tests for the City class"""

    def test_is_subclass(self):
        """City inherits from BaseModel"""
        c = City()
        self.assertIsInstance(c, BaseModel)

    def test_instantiation(self):
        """City can be instantiated"""
        c = City()
        self.assertIsNotNone(c.id)

    def test_to_dict_no_sa_state(self):
        """to_dict does not contain _sa_instance_state"""
        c = City()
        d = c.to_dict()
        self.assertNotIn('_sa_instance_state', d)
        self.assertEqual(d['__class__'], 'City')

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage attribute test only'
    )
    def test_class_attributes(self):
        """state_id and name are class attributes"""
        self.assertIn('state_id', City.__dict__)
        self.assertIn('name', City.__dict__)
