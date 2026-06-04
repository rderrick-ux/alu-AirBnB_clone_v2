#!/usr/bin/python3
"""Unit tests for the State class"""
import os
import unittest
from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    """Tests for the State class"""

    def test_is_subclass(self):
        """State inherits from BaseModel"""
        s = State()
        self.assertIsInstance(s, BaseModel)

    def test_instantiation(self):
        """State can be instantiated"""
        s = State()
        self.assertIsNotNone(s.id)

    def test_to_dict_no_sa_state(self):
        """to_dict does not contain _sa_instance_state"""
        s = State()
        s.name = 'TestState'
        d = s.to_dict()
        self.assertNotIn('_sa_instance_state', d)
        self.assertEqual(d['__class__'], 'State')

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage attribute test only'
    )
    def test_name_class_attribute(self):
        """name is a class attribute for FileStorage"""
        self.assertIn('name', State.__dict__)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage tests only'
    )
    def test_cities_property(self):
        """cities property returns related City instances"""
        from models.city import City
        from models import storage
        state = State()
        state.name = 'California'
        state.save()
        city = City()
        city.state_id = state.id
        city.name = 'San Francisco'
        city.save()
        cities = state.cities
        self.assertIsInstance(cities, list)
        self.assertTrue(any(c.id == city.id for c in cities))
        storage.delete(city)
        storage.delete(state)
        storage.save()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage tests only'
    )
    def test_save_and_retrieve(self):
        """save() persists state to storage"""
        from models import storage
        s = State()
        s.name = 'Nevada'
        s.save()
        key = 'State.{}'.format(s.id)
        self.assertIn(key, storage.all())
        storage.delete(s)
        storage.save()
