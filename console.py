#!/usr/bin/python3
"""A class that inherits from Cmd class
It allows us to interactively and non-interactively:
    - create a data model
    - manage (create, update, destroy, etc) objects via a console / interpreter
    - store and persist objects to a file (JSON file)
"""

import cmd
import json
import sys
import re
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place


class HBNBCommand(cmd.Cmd):
    """class HBNBCommand for CLI """
    valid_classes = {'BaseModel': BaseModel, 'User': User,
                     'Amenity': Amenity, 'City': City, 'State': State,
                     'Place': Place, 'Review': Review}

    Class_missing = '** class name missing **'
    Non_class = "** class doesn't exist **"
    Id_missing = "** instance id missing **"
    Non_id = "** no instance found **"
    Attr_missing = "** attribute name missing **"
    Value_missing = "** value missing **"

    prompt = '(hbnb) '

    def do_help(self, arg):
        """To get help on a command, type help <topic>.
        """
        return super().do_help(arg)

    def do_quit(self, line):
        """Quit command to exit the program """
        return True

    def do_EOF(self):
        """Ends the program """
        return True

    def emptyline(self):
        """Does nothing when empty line is given """
        pass

    def do_create(self, line):
        """Creates a new instance of BaseModel """
        lines = line.split()
        if not line:
            print(HBNBCommand.Class_missing)
        elif line not in HBNBCommand.valid_classes.keys():
            print(HBNBCommand.Non_class)
        else:
            obj = HBNBCommand.valid_classes[lines[0]]()
            obj.save()
            print(obj.id)

    def do_show(self, line):
        """Prints the string representation of an instance.
        """
        lines = line.split()
        if not line:
            print(HBNBCommand.Class_missing)
            return
        elif lines[0] not in HBNBCommand.valid_classes.keys():
            print(HBNBCommand.Non_class)
            return
        elif len(lines) < 2:
            print(HBNBCommand.Id_missing)
            return
        instance_obj = storage.all()
        key = "{}.{}".format(lines[0], lines[1])
        req_instance = instance_obj.get(key, None)
        if req_instance is None:
            print(HBNBCommand.Non_id)
            return
        print(req_instance)

    def do_destroy(self, line):
        """Deletes an instance
        based on the class name and id
        """
        lines = line.split()
        if not line:
            print(HBNBCommand.Class_missing)
            return
        elif lines[0] not in HBNBCommand.valid_classes.keys():
            print(HBNBCommand.Non_class)
            return
        elif len(lines) < 2:
            print(HBNBCommand.Id_missing)
            return
        inst_obj = storage.all()
        key = "{}.{}".format(lines[0], lines[1])
        req_instance = inst_obj.get(key, None)
        if req_instance is None:
            print(HBNBCommand.Non_id)
            return
        del inst_obj[key]
        storage.save()

    def do_all(self, line):
        """Prints string representation of all instances.
        """
        lines = line.split()
        all_objs = storage.all()

        if len(lines) < 1:
            print(["{}".format(str(v)) for _, v in all_objs.items()])
            return
        if lines[0] not in HBNBCommand.valid_classes.keys():
            print(HBNBCommand.Non_class)
            return
        else:
            print(["{}".format(str(v))
                  for k, v in all_objs.items()
                  if type(v).__name__ == lines[0]])
            return

    def do_update(self, line):
        """ Updates an instance based on the class name and id """
        lines = line.split()
        if not line:
            print(HBNBCommand.Class_missing)
            return
        if lines[0] not in HBNBCommand.valid_classes:
            print(HBNBCommand.Non_class)
            return
        elif len(lines) < 2:
            print(HBNBCommand.Id_missing)
            return
        instance_objs = storage.all()
        key = "{}.{}".format(lines[0], lines[1])
        req_instance = instance_objs.get(key, None)
        if req_instance is None:
            print(HBNBCommand.Non_id)
            return

        match_json = re.findall(r"{.*}", line)
        if match_json:
            payload = None
            try:
                payload: dict = json.loads(match_json[0])
            except Exception:
                print("** invalid syntax")
                return
            for k, v in payload.items():
                setattr(req_instance, k, v)
            storage.save()
            return
        if len(lines) < 3:
            print(HBNBCommand.Attr_missing)
            return
        if len(lines) < 4:
            print(HBNBCommand.Value_missing)
            return
        first_attr = re.findall(r"^[\"\'](.*?)[\"\']", lines[3])
        if first_attr:
            setattr(req_instance, lines[2], first_attr[0])
        else:
            value_list = lines[3].split()
            setattr(req_instance, lines[2], parse_str(value_list[0]))
        storage.save()

    def is_float(x):
        """Checks if `x` is float.
        """
        try:
            a = float(x)
        except (TypeError, ValueError):
            return False
        else:
            return True

    def is_int(x):
        """Checks if `x` is int.
        """
        try:
            a = float(x)
            b = int(a)
        except (TypeError, ValueError):
            return False
        else:
            return a == b

    def parse_str(arg):
        """Parse `arg` to an `int`, `float` or `string`.
        """
        parsed = re.sub("\"", "", arg)

        if is_int(parsed):
            return int(parsed)
        elif is_float(parsed):
            return float(parsed)
        else:
            return arg


if __name__ == '__main__':
    HBNBCommand().cmdloop()
