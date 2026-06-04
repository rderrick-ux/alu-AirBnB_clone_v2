#!/usr/bin/python3
"""Unit tests for the DBStorage class"""
import os
import unittest


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') != 'db',
    'DBStorage tests only'
)
class TestDBStorageInstantiation(unittest.TestCase):
    """Tests for DBStorage class docstrings and structure"""

    def test_module_docstring(self):
        """db_storage module has a docstring"""
        import models.engine.db_storage as db_mod
        self.assertIsNotNone(db_mod.__doc__)

    def test_class_docstring(self):
        """DBStorage class has a docstring"""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.__doc__)

    def test_all_docstring(self):
        """all() method has a docstring"""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.all.__doc__)

    def test_new_docstring(self):
        """new() method has a docstring"""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.new.__doc__)

    def test_save_docstring(self):
        """save() method has a docstring"""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.save.__doc__)

    def test_delete_docstring(self):
        """delete() method has a docstring"""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.delete.__doc__)

    def test_reload_docstring(self):
        """reload() method has a docstring"""
        from models.engine.db_storage import DBStorage
        self.assertIsNotNone(DBStorage.reload.__doc__)


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') != 'db',
    'DBStorage tests only'
)
class TestDBStorageAll(unittest.TestCase):
    """Tests for DBStorage.all()"""

    def setUp(self):
        from models import storage
        self.storage = storage

    def test_all_returns_dict(self):
        """all() returns a dict"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_all_with_state_class(self):
        """all(State) returns only State objects"""
        from models.state import State
        result = self.storage.all(State)
        for obj in result.values():
            self.assertIsInstance(obj, State)

    def test_all_with_string_class_name(self):
        """all('State') filters correctly"""
        from models.state import State
        result = self.storage.all('State')
        for obj in result.values():
            self.assertIsInstance(obj, State)

    def test_all_keys_format(self):
        """all() keys are in ClassName.id format"""
        from models.state import State
        state = State(name='KeyFormatTest')
        state.save()
        result = self.storage.all(State)
        for key in result.keys():
            parts = key.split('.')
            self.assertEqual(len(parts), 2)
        self.storage.delete(state)
        self.storage.save()


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') != 'db',
    'DBStorage tests only'
)
class TestDBStorageNewSaveDelete(unittest.TestCase):
    """Tests for DBStorage.new(), save(), and delete()"""

    def setUp(self):
        from models import storage
        self.storage = storage

    def _db_connect(self):
        import MySQLdb
        return MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST', 'localhost'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )

    def _count_table(self, table):
        conn = self._db_connect()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM {}'.format(table))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count

    def test_new_and_save_increments_db(self):
        """Creating a State increases states table count by 1"""
        from models.state import State
        before = self._count_table('states')
        state = State(name='DBTest_NewSave')
        state.save()
        after = self._count_table('states')
        self.assertEqual(after, before + 1)
        self.storage.delete(state)
        self.storage.save()

    def test_save_commits_to_db(self):
        """save() persists data visible via direct SQL"""
        from models.state import State
        state = State(name='DBTest_Commit')
        state.save()
        conn = self._db_connect()
        cur = conn.cursor()
        cur.execute('SELECT name FROM states WHERE id = %s', (state.id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], 'DBTest_Commit')
        self.storage.delete(state)
        self.storage.save()

    def test_delete_removes_from_db(self):
        """delete() + save() decrements the states table count"""
        from models.state import State
        state = State(name='DBTest_Delete')
        state.save()
        before = self._count_table('states')
        self.storage.delete(state)
        self.storage.save()
        after = self._count_table('states')
        self.assertEqual(after, before - 1)

    def test_delete_none_does_nothing(self):
        """delete(None) does not raise or modify storage"""
        from models.state import State
        before = len(self.storage.all(State))
        self.storage.delete(None)
        after = len(self.storage.all(State))
        self.assertEqual(before, after)

    def test_delete_removes_from_all(self):
        """Deleted object no longer appears in all()"""
        from models.state import State
        state = State(name='DBTest_DeleteAll')
        state.save()
        key = 'State.{}'.format(state.id)
        self.assertIn(key, self.storage.all(State))
        self.storage.delete(state)
        self.storage.save()
        self.assertNotIn(key, self.storage.all(State))


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') != 'db',
    'DBStorage tests only'
)
class TestDBStorageConsoleIntegration(unittest.TestCase):
    """Integration tests: console create commands hit the database"""

    def setUp(self):
        from models import storage
        self.storage = storage

    def _db_count(self, table):
        import MySQLdb
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST', 'localhost'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM {}'.format(table))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count

    def test_console_create_state_increments_db(self):
        """console 'create State' adds a record to states table"""
        from io import StringIO
        from unittest.mock import patch
        from console import HBNBCommand
        before = self._db_count('states')
        with patch('sys.stdout', new=StringIO()) as mock_out:
            HBNBCommand().onecmd('create State name="ConsoleTestState"')
            obj_id = mock_out.getvalue().strip()
        after = self._db_count('states')
        self.assertEqual(after, before + 1)
        state = self.storage.all('State').get('State.{}'.format(obj_id))
        if state:
            self.storage.delete(state)
            self.storage.save()

    def test_console_create_user_increments_db(self):
        """console 'create User' adds a record to users table"""
        from io import StringIO
        from unittest.mock import patch
        from console import HBNBCommand
        before = self._db_count('users')
        with patch('sys.stdout', new=StringIO()) as mock_out:
            HBNBCommand().onecmd(
                'create User email="dbtest@test.com" password="pwd"'
            )
            obj_id = mock_out.getvalue().strip()
        after = self._db_count('users')
        self.assertEqual(after, before + 1)
        user = self.storage.all('User').get('User.{}'.format(obj_id))
        if user:
            self.storage.delete(user)
            self.storage.save()
