#!/usr/bin/python3
"""Defines unittests for console.py.
"""
from io import StringIO
import os
import unittest
from unittest.mock import patch
from console import HBNBCommand
from models import storage
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestBaseModel(unittest.TestCase):
    """Testing `Basemodel `commands.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_create_basemodel(self):
        """Test create basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create BaseModel')
            self.assertIsInstance(f.getvalue().strip(), str)
            self.assertIn("BaseModel.{}".format(
                f.getvalue().strip()), storage.all().keys())

    def test_all_basemodel(self):
        """Test all basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all BaseModel')
            for item in json.loads(f.getvalue()):
                self.assertEqual(item.split()[0], '[BaseModel]')

    def test_show_basemodel(self):
        """Test show basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.eyes = "green"
            HBNBCommand().onecmd(f'show BaseModel {b1.id}')
            res = f"[{type(b1).__name__}] ({b1.id}) {b1.__dict__}"
            self.assertEqual(f.getvalue().strip(), res)

    def test_update_basemodel(self):
        """Test update basemodel object.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.name = "Cecilia"
            HBNBCommand().onecmd(f'update BaseModel {b1.id} name "Ife"')
            self.assertEqual(b1.__dict__["name"], "Ife")

        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.age = 75
            HBNBCommand().onecmd(f'update BaseModel {b1.id} age 25')
            self.assertIn("age", b1.__dict__.keys())
            self.assertEqual(b1.__dict__["age"], 25)

        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.savings = 25.67
            HBNBCommand().onecmd(f'update BaseModel {b1.id} savings 35.89')
            self.assertIn("savings", b1.__dict__.keys())
            self.assertEqual(b1.__dict__["savings"], 35.89)

        with patch('sys.stdout', new=StringIO()) as f:
            b1 = BaseModel()
            b1.age = 60
            cmmd = f'update BaseModel {b1.id} age 10 color "green"'
            HBNBCommand().onecmd(cmmd)
            self.assertIn("age", b1.__dict__.keys())
            self.assertNotIn("color", b1.__dict__.keys())
            self.assertEqual(b1.__dict__["age"], 10)

    def test_destroy_basemodel(self):
        """Test destroy basemodel object.
        """
        with patch('sys.stdout', new=StringIO()):
            bm = BaseModel()
            HBNBCommand().onecmd(f'destroy BaseModel {bm.id}')
            self.assertNotIn("BaseModel.{}".format(
                bm.id), storage.all().keys())
