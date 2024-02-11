#!/usr/bin/python
"""Defines a BaseModel class """

import uuid
import datetime
import models


class BaseModel:
    """Base class which defines other methods and classes

      public instance attributes:
           id(str): provides uniqe id for a specific user
           created_at: assigns current datetime
           updated_at: updates the current datetime

      Methods:
           __str__: prints string representation of the class
           save(self): update instance attribute
                       with the current datetime
           to_dict(self): return the dictionary representation of an instance
    """

    def __init__(self, *args, **kwargs):
        """initializes id, created_at, updated_at """
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
                    self.__dict__[key] = dat
                elif key[0] == "id":
                    self.__dict__[key] = str(value)
                else:
                    self.__dict__[key] = value

    def save(self):
        """updates the instance attribute with the current date """
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing
        all keys/values of __dict__ of the instance:
        """
        dic = {}
        for k, v in self.__dict__.items():
            if k == 'created_at' or k == 'updated_at':
                dic[k] = v.isoformat()
            else:
                dic[k] = v
        dic['__class__'] = self.__class__.__name__
        return dic

    def __str__(self):
        """returns [<class name>] (<self.id>) <self.__dict__> """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)
