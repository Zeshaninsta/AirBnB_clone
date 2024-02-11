#!/usr/bin/python
"""Defines a BaseModel class"""

import uuid
import datetime
import models


class BaseModel:
    """Base class that defines common methods and attributes.

    Public instance attributes:
        id (str): Provides a unique ID for a specific instance.
        created_at: Assigns the current datetime at the time of instance creation.
        updated_at: Updates to the current datetime whenever the instance is modified.

    Methods:
        __str__: Returns a string representation of the class.
        save(self): Updates the instance attribute with the current datetime.
        to_dict(self): Returns a dictionary representation of an instance.
    """

    def __init__(self, *args, **kwargs):
        """Initializes id, created_at, and updated_at."""
        date_format = '%Y-%m-%dT%H:%M:%S.%f'
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            models.storage.new(self)
        else:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    dat = datetime.datetime.strptime(value, date_format)
                    setattr(self, key, dat)
                elif key == "id":
                    setattr(self, key, str(value))
                else:
                    setattr(self, key, value)

    def save(self):
        """Updates the instance attribute with the current date."""
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__ of the instance."""
        dic = {k: v.isoformat() if isinstance(v, datetime.datetime) else v for k, v in self.__dict__.items() if k not in ["__class__"]}
        dic['__class__'] = self.__class__.__name__
        return dic

    def __str__(self):
        """Returns [<class name>] (<self.id>) <self.__dict__>"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

