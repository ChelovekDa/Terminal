import os
import random
import json
from os import path
import datetime

from based.gate import Gate, Logger

names = []

class _based():

    def __init__(self, clazz):
        self.clazz = clazz

class _Items():

    def __iter__(self) -> list[str]:
        lis = []
        for i in range(len(self.items)):
            lis.append(_Item().str(self.items[i]))
        return lis

    def __init__(self, items: list[_based]):
        self.items = items

    def append(self, obj: _based):
        self.items.append(obj)

    def remove(self, obj: _based):
        self.items.remove(obj)

class _Room():

    def __init__(self, items: _Items([]) = _Items([]), name = "", blocked = False):
        self.items = items
        self.name = name
        self.blocked = blocked

    def set_name(self, name: str):
        self.name = name

class _Floor():

    def __init__(self, rooms: list[_Room]):
        self.rooms = rooms

    def append(self, obj: _Room):
        self.rooms.append(obj)

class _Building():

    def __init__(self, floors: list[_Floor]):
        self.floors = floors

    def append(self, obj: _Floor):
        self.floors.append(obj)

class _Level():

    def __gen_name(self) -> str:
        return f"NewWorld-{str(datetime.datetime.now().year)}-{str(datetime.datetime.now().month)}-{str(datetime.datetime.now().day)}-{str(datetime.datetime.now().hour)}-{str(datetime.datetime.now().minute)}-{str(datetime.datetime.now().second)}"

    def __init__(self, buildings: list[_Building], name: str = ""):
        self.buildings = buildings
        if (name == ""):
            name = self.__gen_name()
        self.name = name

    def get_names(self) -> list[str]:
        return names

    def append(self, obj: _Building):
        self.buildings.append(obj)

    def str(self) -> dict:
        dic = {}
        level = self
        for i, building in enumerate(level.buildings):
            build = {}
            for k, floor in enumerate(building.floors):
                fl = {}
                for room in floor.rooms:
                    room_dict = {}
                    room_dict["name"] = room.name
                    room_dict["blocked"] = room.blocked
                    items = []
                    for item in room.items.__iter__():
                        items.append(item)
                    room_dict["items"] = items
                    fl[room.name] = room_dict
                build[str(k)] = dict(fl)
            dic[str(i)] = dict(build)
        return dic

    def _to_json(self):
        dic = self.str()

        direc = f"{Gate().get_base_directory()}/Terminal/Levels"
        if (path.exists(direc)):
            open(f"{direc}/{self.name}.json", "w").close()
            with open(f"{direc}/{self.name}.json", "w") as write_file:
                json.dump(dic, write_file)
        else:
            os.mkdir(direc)
            with open(f"{direc}/{self.name}.json", "w") as write_file:
                json.dump(dic, write_file)

        open(f"backend/preFiles/app/activate.json", "w").close()
        with open(f"backend/preFiles/app/activate.json", "w") as write_file:
            json.dump(dic, write_file)
        Logger().log(f"Was been saved a new level without keys set. Site: {self.name}")

    def _set_keys(self):
        data = {}
        def get_count() -> int:
            count = 0
            for build in data.keys():
                build_dict = dict(data.get(build))
                for floor in build_dict.keys():
                    floor_dict = dict(build_dict.get(floor))
                    for room in floor_dict.keys():
                        room_dict = dict(floor_dict.get(room))
                        count += list(room_dict.get("items")).count("Key")
                        if (count == 0):
                            continue
                        else:
                            chance = random.randint(1,2)
                            if (chance == 1):
                                if (list(room_dict.get("items")).count("Key") > 0):
                                    continue
                                else:
                                    room_dict["blocked"] = True
                                    floor_dict[room] = room_dict
                                    build_dict[floor] = floor_dict
                                    data[build] = build_dict
                                    count = count - 1
                            else:
                                continue
            return count

        with open("backend/preFiles/app/activate.json", "r") as read_file:
            data = json.load(read_file)
        data = dict(data)
        ifel = get_count()
        while int(ifel) >= 1:
            ifel = get_count()
        open(f"backend/preFiles/app/activate.json", "w").close()
        with open(f"backend/preFiles/app/activate.json", "w") as write_file:
            json.dump(data, write_file)
        Logger().log(f"Was been saved a new level with key set and lock rooms. Site: {self.name}")

class _Item():

    class Key(_based):
        def __init__(self, room: _Room = _Room(), code: int = 0):
            super().__init__(self)
            self.backRoom = room
            self.code = code

    class Lockpick(_based):

        def __init__(self):
            super().__init__(self)

        def worked(self) -> bool:
            if (random.randint(0, 9) == 3 or 7):
                return True
            else:
                return False

    class Document(_based):
        def __init__(self, information: str = "", name = ""):
            super().__init__(self)
            self.info = information
            self.name = name

    class Paper(_based):
        def __init__(self):
            super().__init__(self)
    class Toilet_paper(_based):
        def __init__(self):
            super().__init__(self)
    class Poop(_based):
        def __init__(self):
            super().__init__(self)

        def sound(self) -> str:
            return "poop"
    class Stair(_based):
        def __init__(self):
            super().__init__(self)
    class Sofa(_based):
        def __init__(self):
            super().__init__(self)
    class Table(_based):
        def __init__(self):
            super().__init__(self)
    class Syringe(_based):
        def __init__(self):
            super().__init__(self)
    class Waste(_based):
        def __init__(self):
            super().__init__(self)

    def __get_catalogue(self) -> dict[str: _based]:
        catalogue = {
            "Key": self.Key(),
            "Lockpick": self.Lockpick(),
            "Document": self.Document(),
            "Paper": self.Paper(),
            "Toilet_paper": self.Toilet_paper(),
            "Poop": self.Poop(),
            "Stair": self.Stair(),
            "Sofa": self.Sofa(),
            "Table": self.Table(),
            "Syringe": self.Syringe(),
            "Waste": self.Waste()
        }
        return catalogue

    def str(self, obj: _based) -> str:
        catalogue = {
            self.Key: "Key",
            self.Lockpick: "Lockpick",
            self.Document: "Document",
            self.Paper: "Paper",
            self.Toilet_paper: "Toilet_paper",
            self.Poop: "Poop",
            self.Stair: "Stair",
            self.Sofa: "Sofa",
            self.Table: "Table",
            self.Syringe: "Syringe",
            self.Waste: "Waste"
        }
        return catalogue.get(type(obj))

    def get_random_item(self) -> _based:
        return self.__get_catalogue().get(random.choice(list(self.__get_catalogue().keys())))

class Generate():

    def __generate_room_name(self) -> str:
        global names
        name = random.choice("QWERTYUIOPASDFGHJKLZXCVBNM")
        name = name + (str(random.randint(1, 9)))
        if (name not in names):
            names.append(name)
            return name
        else:
            return self.__generate_room_name()

    def __generate_items(self, count: int) -> _Items:
        items = _Items([])
        for i in range(count):
            items.append(_Item().get_random_item())
        return items

    def __generate_new_seed(self) -> str:
        seed = ""
        seed = seed + (str(random.randint(1, 5))) # buildings
        seed = seed + (str(random.randint(1, 9))) # floors
        seed = seed + (str(random.randint(3, 5))) # rooms
        return seed

    def generate(self) -> _Level:
        """
        Main func for return already completed level.
        :return: Level
        """
        level = _Level([])
        for buildings in range(int(self.seed[0])):
            build = _Building([])
            for floors in range(int(self.seed[1])):
                floor = _Floor([])
                for rooms in range(int(self.seed[2])):
                    if (random.randint(0, 9) in [2, 5, 9, 1]):
                        room = _Room(
                            self.__generate_items(random.randint(0, 2)),
                            self.__generate_room_name())
                    else:
                        room = _Room(
                            [],
                            self.__generate_room_name())
                    floor.append(room)
                build.append(floor)
            level.append(build)
        level._to_json()
        level._set_keys()
        return level

    def __init__(self):
        self.seed = self.__generate_new_seed()


