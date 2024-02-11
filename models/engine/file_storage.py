#!/usr/bin/python3
"""Defines a class FileStorage
"""

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place
import os
import json


class FileStorage():
    """serializes instances to a JSON file
    and deserializes JSON file to instances

    Private class attributes:
       __file_path: a path to a file
       __objects: a dictionary

    Public instance methods:
       all(self): returns the dictionary __objects
       new(self, obj): sets in __objects the obj with key <obj class name>.id
        save(self): serializes __objects to the JSON file (path: __file_path)
       reload(self): deserializes the JSON file to __objects
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returns the dictionaty __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """
           sets in __objects the obj with key <obj class name>.id
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file """
        with open(FileStorage.__file_path, 'w') as js:
            json.dump(
                {k: v.to_dict() for k, v in FileStorage.__objects.items()}, js)

    def reload(self):
        """Deserializes the Json file"""

        current_classes = {'BaseModel': BaseModel, 'User': User,
                           'Amenity': Amenity, 'City': City, 'State': State,
                           'Place': Place, 'Review': Review}

        if not os.path.exists(FileStorage.__file_path):
            return

        des = None
        try:
            with open(FileStorage.__file_path, "r") as jr:
                des = json.load(jr)
        except Exception:
            pass
        if des is None:
            return
        FileStorage.__objects = {
                k: current_classes[k.split('.')[0]](**v)
                for k, v in des.items()}
