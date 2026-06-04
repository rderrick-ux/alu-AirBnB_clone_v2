#!/usr/bin/python3
"""Unit tests for the HBNBCommand console"""
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place


class TestConsoleDoCreate(unittest.TestCase):
    """Tests for the do_create command"""

    def test_create_no_class(self):
        """create with no class name prints error"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create')
            self.assertIn('** class name missing **', f.getvalue())

    def test_create_invalid_class(self):
        """create with unknown class prints error"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create NonExistent')
            self.assertIn("** class doesn't exist **", f.getvalue())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage tests only'
    )
    def test_create_state_string_param(self):
        """create State with string param sets name"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="California"')
            obj_id = f.getvalue().strip()
        key = 'State.{}'.format(obj_id)
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].name, 'California')
        storage.delete(storage.all()[key])
        storage.save()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage tests only'
    )
    def test_create_underscore_replaced_with_space(self):
        """underscores in string params are replaced by spaces"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="New_York"')
            obj_id = f.getvalue().strip()
        key = 'State.{}'.format(obj_id)
        self.assertEqual(storage.all()[key].name, 'New York')
        storage.delete(storage.all()[key])
        storage.save()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage tests only'
    )
    def test_create_integer_param(self):
        """create with integer param sets attribute"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                'create Place city_id="0001" user_id="0001" '
                'name="Test" number_rooms=3'
            )
            obj_id = f.getvalue().strip()
        key = 'Place.{}'.format(obj_id)
        self.assertEqual(storage.all()[key].number_rooms, 3)
        storage.delete(storage.all()[key])
        storage.save()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage tests only'
    )
    def test_create_float_param(self):
        """create with float param sets attribute"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                'create Place city_id="0001" user_id="0001" '
                'name="Test" latitude=37.773972'
            )
            obj_id = f.getvalue().strip()
        key = 'Place.{}'.format(obj_id)
        self.assertAlmostEqual(
            storage.all()[key].latitude, 37.773972, places=5
        )
        storage.delete(storage.all()[key])
        storage.save()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage tests only'
    )
    def test_create_skips_invalid_params(self):
        """invalid parameters are silently skipped"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                'create State name="Valid" bad_param invalid=value'
            )
            obj_id = f.getvalue().strip()
        key = 'State.{}'.format(obj_id)
        self.assertEqual(storage.all()[key].name, 'Valid')
        storage.delete(storage.all()[key])
        storage.save()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage tests only'
    )
    def test_create_all_param_types(self):
        """create Place with string, int, and float params"""
        cmd = (
            'create Place city_id="0001" user_id="0001" '
            'name="My_little_house" number_rooms=4 number_bathrooms=2 '
            'max_guest=10 price_by_night=300 '
            'latitude=37.773972 longitude=-122.431297'
        )
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
            obj_id = f.getvalue().strip()
        key = 'Place.{}'.format(obj_id)
        place = storage.all()[key]
        self.assertEqual(place.name, 'My little house')
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.max_guest, 10)
        self.assertAlmostEqual(place.latitude, 37.773972, places=5)
        self.assertAlmostEqual(place.longitude, -122.431297, places=5)
        storage.delete(place)
        storage.save()

    def test_create_returns_valid_uuid(self):
        """create prints a valid UUID"""
        import uuid
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="UUIDTest"')
            obj_id = f.getvalue().strip()
        try:
            uuid.UUID(obj_id)
            valid = True
        except ValueError:
            valid = False
        self.assertTrue(valid)
        key = 'State.{}'.format(obj_id)
        if key in storage.all():
            storage.delete(storage.all()[key])
            storage.save()


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') == 'db',
    'FileStorage console tests only'
)
class TestConsoleAllCommand(unittest.TestCase):
    """Tests for the do_all command"""

    def test_all_no_class(self):
        """all with no class returns a list"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all')
            self.assertTrue(f.getvalue().strip().startswith('['))

    def test_all_valid_class(self):
        """all with valid class returns a list"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all State')
            self.assertTrue(f.getvalue().strip().startswith('['))

    def test_all_invalid_class(self):
        """all with invalid class prints error"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all InvalidClass')
            self.assertIn("** class doesn't exist **", f.getvalue())


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') == 'db',
    'FileStorage console tests only'
)
class TestConsoleDestroyCommand(unittest.TestCase):
    """Tests for the do_destroy command"""

    def test_destroy_no_class(self):
        """destroy with no class prints error"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy')
            self.assertIn('** class name missing **', f.getvalue())

    def test_destroy_invalid_class(self):
        """destroy with invalid class prints error"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy Fake')
            self.assertIn("** class doesn't exist **", f.getvalue())

    def test_destroy_no_id(self):
        """destroy with no id prints error"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy State')
            self.assertIn('** instance id missing **', f.getvalue())

    def test_destroy_removes_object(self):
        """destroy removes the object from storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="ToDestroy"')
            obj_id = f.getvalue().strip()
        key = 'State.{}'.format(obj_id)
        self.assertIn(key, storage.all())
        HBNBCommand().onecmd('destroy State {}'.format(obj_id))
        self.assertNotIn(key, storage.all())
