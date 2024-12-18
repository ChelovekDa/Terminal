import os
import random
import json
from os import path
import datetime

import based
from based.Logger import stack, Logger
from based.based_values import values

names = []

class _based():

    def __init__(self, clazz):
        self.clazz = clazz

    def __str__(self) -> str:
        return ""

    def to_dict(self) -> dict:
        pass

class Items():

    def __iter__(self) -> list:
        """Return this list of items in room but in list[str] view."""
        lis = []
        for i in range(len(self.items)):
            lis.append(Item().str(self.items[i]))
        return lis

    def __liter__(self) -> list[str]:
        """Return this list of items in room but in list[str] view, where everyone from elements in lower register."""
        lis = []
        for i in range(len(self.items)):
            lis.append(Item().str(self.items[i]).lower())
        return lis

    def __init__(self, items: list[_based]):
        self.items = list(items)

    def __getitem__(self, index) -> _based:
        for i, item in enumerate(self.items):
            if i == index:
                return item
        return None

    def __len__(self) -> int:
        """Return the length of items list"""
        item = _based(None)
        i = 0
        for item in self.items:
            i+=1
        del item
        return i

    def append(self, obj: _based):
        self.items.append(obj)

    def remove(self, obj: _based):
        self.items.remove(obj)

class Room():

    def __init__(self, items: Items([]) = Items([]), name = "", blocked = False):
        self.items = items
        self.name = name
        self.blocked = blocked

    def set_name(self, name: str):
        self.name = name

class Floor():

    def __init__(self, rooms: list[Room]):
        self.rooms = rooms

    def append(self, obj: Room):
        self.rooms.append(obj)

    def __get_room_names(self) -> list[str]:
        names = []
        for room in self.rooms:
            names.append(room.name)
        return names

    def __contains__(self, room_name: str) -> bool:
        return room_name in self.__get_room_names()

    def __get__(self, room_name: str) -> Room:
        if self.__contains__(room_name):
            for room in self.rooms:
                if (room.name == room_name):
                    return room
        else:
            return Room([], "", True)

class Building():

    def __init__(self, floors: list[Floor]):
        self.floors = floors

    def append(self, obj: Floor):
        self.floors.append(obj)

class Level():

    def gen_name(self) -> str:
        return f"NewWorld-{str(datetime.datetime.now().year)}-{str(datetime.datetime.now().month)}-{str(datetime.datetime.now().day)}-{str(datetime.datetime.now().hour)}-{str(datetime.datetime.now().minute)}-{str(datetime.datetime.now().second)}"

    def __init__(self, buildings: list[Building], name: str = "", requirement: _based = _based(None)):
        global Item
        self.buildings = buildings
        if (name == ""):
            name = self.gen_name()
        self.name = name
        if (requirement.clazz == None):
            requirement = self.generate_finish_requirement()
        self.req = requirement

    def unlock_all_doors(self):
        for building in self.buildings:
            build = building
            for floor in build.floors:
                floo = floor.rooms
                for room in floo:
                    room.blocked = False

    def generate_finish_requirement(self) -> _based:
        """
        This func setting a finish requirement needs to finish the level
        NOTE: Everyone level has a single requirement to finish level.

        :return: Set the requirement of finish level
        """
        return Item().Document(name="TOP SECRET", information="TOP SECRET", important=True)

    def get_names(self) -> list[str]:
        return names

    def append(self, obj: Building):
        self.buildings.append(obj)

    def str(self) -> dict:
        dic = {}
        for i, building in enumerate(self.buildings):
            build = {}
            for k, floor in enumerate(building.floors):
                fl = {}
                for room in floor.rooms:
                    room_dict = {}
                    room_dict["name"] = room.name
                    room_dict["blocked"] = room.blocked
                    if (room.items.__len__() != 0):
                        items = []
                        for i in range(room.items.__len__()):
                            obj = room.items.__getitem__(i)
                            if (type(obj) == type(Item().Document())):
                                items.append({
                                    Item().str(obj): {"type": Item().str(obj), "information": obj.info, "name": obj.name, "important": obj.important}
                                })
                            else:
                                items.append({
                                    Item().str(obj): {"type": Item().str(obj)}
                                })
                        room_dict["items"] = items
                    else:
                        room_dict["items"] = []
                    fl[room.name] = room_dict
                build[str(k)] = dict(fl)
            dic[str(i)] = dict(build)
        #dic["target"] = self.req.to_dict()
        return dic

    def to_json(self, dic: dict = None):
        if (dic == None):
            dic = self.str()
        data = dic

        direc = f"{values().get_base_directory()}/Terminal/Levels"
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
                if (build == "target"):
                    break
                build_dict = dict(data.get(build))
                for floor in build_dict.keys():
                    floor_dict = dict(build_dict.get(floor))
                    for room in floor_dict.keys():
                        room_dict = dict(floor_dict.get(room))
                        for item in list(room_dict.get("items")):
                            if (dict(item).get("Key") != None):
                                count+=1
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

class Item():

    class Key(_based):
        def __init__(self, room: Room = Room()):
            super().__init__(self)
            self.backRoom = room

    class Lockpick(_based):

        def __init__(self):
            super().__init__(self)

        def worked(self) -> bool:
            if (random.randint(0, 9) == 3 or 7):
                return True
            else:
                return False

    class Document(_based):
        def __init__(self, information: str = "", name = "", important: bool = False):
            super().__init__(self)
            self.info = information
            self.name = name
            self.important = important

        def to_dict(self) -> dict:
            return {
                "Document": {"type": Item().str(Item.Document()), "information": self.info, "important": self.important,
                             "name": self.name}}

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
        cat = dict(self.__get_catalogue())
        for key in cat.keys():
            if (type(cat.get(key)) == type(obj)):
                return key
        del cat
        return None

    def get_random_item(self) -> _based:
        return self.__get_catalogue().get(random.choice(list(self.__get_catalogue().keys())))

    def get_list_items(self) -> list[str]:
        return list(dict(self.__get_catalogue()).keys())

class Generate():

    def __generate_room_name(self) -> str:
        global names
        name = f"{random.choice("QWERTYUIOPASDFGHJKLZXCVBNM")}{str(random.randint(1, 9))}"
        if (name not in names):
            names.append(name)
            return name
        else:
            return self.__generate_room_name()

    def __generate_room_name_for_HARD(self) -> str:
        global names
        name = f"{random.choice("QWERTYUIOPASDFGHJKLZXCVBNM")}{str(random.randint(1, 99))}"
        if (name not in names):
            names.append(name)
            return name
        else:
            return self.__generate_room_name_for_HARD()

    def base_val(self) -> str:
        """
        This func called when was arrived the "maximum recursion depth exceeded" error.
        :return: str with name of room.
        """
        global names
        for alp in "QWERTYUIOPASDFGHJKLZXCVBNM":
            for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                if (names.count(f"{alp}{str(i)}") != 1):
                    names.append(f"{alp}{str(i)}")
                    return f"{alp}{str(i)}"
                else:
                    continue

    def __generate_items(self, count: int) -> Items:
        items = Items([])
        for i in range(count):
            items.append(Item().get_random_item())
        return items

    def __generate_new_seed(self) -> str:
        seed = ""
        if (self.dif == 1):
            seed = seed + (str(random.randint(1, 2))) # buildings
            seed = seed + (str(random.randint(1, 5))) # floors
            seed = seed + (str(random.randint(3, 7))) # rooms
        elif (self.dif == 2):
            seed = seed + (str(random.randint(2, 5)))  # buildings
            seed = seed + (str(random.randint(4, 9)))  # floors
            seed = seed + (str(random.randint(3, 5)))  # rooms
        elif(self.dif == 3):
            seed = seed + (str(random.randint(5, 10)))  # buildings
            seed = seed + (str(random.randint(9, 18)))  # floors
            seed = seed + (str(random.randint(6, 10)))  # rooms
        else:
            self.dif = 2
            seed = self.__generate_new_seed()
        return seed

    def generate(self) -> Level:
        """
        Main func for return already completed level.
        :return: Level
        """
        global names
        names = []
        level = Level
        if (self.name != ""):
            level = Level([], name=self.name)
        else:
            level = Level([])
        for buildings in range(int(self.seed[0])):
            build = Building([])
            for floors in range(int(self.seed[1])):
                floor = Floor([])
                for rooms in range(int(self.seed[2])):
                    if (random.randint(0, 9) in [2, 5, 9, 1]):
                        if (self.dif == 3):
                            if (random.randint(1, 99) in [10, 26, 83, 16, 93, 27, 83, 41]):
                                room = Room(
                                    self.__generate_items(5),
                                    self.__generate_room_name_for_HARD())
                            else:
                                room = Room(
                                    self.__generate_items(random.randint(1, 3)),
                                    self.__generate_room_name_for_HARD())
                        else:
                            room = Room(
                                self.__generate_items(random.randint(0, 2)),
                                self.__generate_room_name())
                    else:
                        if (self.dif == 3):
                            room = Room(
                                [],
                                self.__generate_room_name_for_HARD())
                        else:
                            room = Room(
                                [],
                                self.__generate_room_name())
                    floor.append(room)
                build.append(floor)
            level.append(build)
        level.to_json()
        level._set_keys()
        stack().controller({values().get_base_level_name_stack_cont(): level.name})
        return level

    def __init__(self, difficulty: int = 2, name: str = ""):
        self.dif = difficulty
        self.seed = self.__generate_new_seed()
        self.Logger = based.gate.Logger()
        self.name = name



