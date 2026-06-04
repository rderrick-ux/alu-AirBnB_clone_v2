#!/usr/bin/python3
"""Unit tests for the Place class"""
import os
import unittest
from models.place import Place
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):
    """Tests for the Place class"""

    def test_is_subclass(self):
        """Place inherits from BaseModel"""
        p = Place()
        self.assertIsInstance(p, BaseModel)

    def test_instantiation(self):
        """Place can be instantiated"""
        p = Place()
        self.assertIsNotNone(p.id)

    def test_to_dict_no_sa_state(self):
        """to_dict does not contain _sa_instance_state"""
        p = Place()
        d = p.to_dict()
        self.assertNotIn('_sa_instance_state', d)
        self.assertEqual(d['__class__'], 'Place')

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage attribute test only'
    )
    def test_class_attributes(self):
        """Place has expected class attributes"""
        for attr in ['city_id', 'user_id', 'name', 'description',
                     'number_rooms', 'number_bathrooms', 'max_guest',
                     'price_by_night', 'latitude', 'longitude']:
            self.assertIn(attr, Place.__dict__)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage tests only'
    )
    def test_amenities_getter(self):
        """amenities getter returns a list"""
        p = Place()
        self.assertIsInstance(p.amenities, list)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage tests only'
    )
    def test_amenities_setter(self):
        """amenities setter appends amenity id"""
        from models.amenity import Amenity
        p = Place()
        a = Amenity()
        a.name = 'Wifi'
        p.amenities = a
        self.assertIn(a.id, p.amenity_ids)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage tests only'
    )
    def test_reviews_getter(self):
        """reviews getter returns a list"""
        p = Place()
        self.assertIsInstance(p.reviews, list)
