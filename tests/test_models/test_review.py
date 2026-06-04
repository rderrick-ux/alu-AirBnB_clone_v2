#!/usr/bin/python3
"""Unit tests for the Review class"""
import os
import unittest
from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):
    """Tests for the Review class"""

    def test_is_subclass(self):
        """Review inherits from BaseModel"""
        r = Review()
        self.assertIsInstance(r, BaseModel)

    def test_instantiation(self):
        """Review can be instantiated"""
        r = Review()
        self.assertIsNotNone(r.id)

    def test_to_dict_no_sa_state(self):
        """to_dict does not contain _sa_instance_state"""
        r = Review()
        d = r.to_dict()
        self.assertNotIn('_sa_instance_state', d)
        self.assertEqual(d['__class__'], 'Review')

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage attribute test only'
    )
    def test_class_attributes(self):
        """place_id, user_id, text are class attributes"""
        self.assertIn('place_id', Review.__dict__)
        self.assertIn('user_id', Review.__dict__)
        self.assertIn('text', Review.__dict__)
