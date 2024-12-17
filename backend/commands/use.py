from backend.funcs.generate_play_space import *
from backend.commands.commandLine import line
from backend.commands.basedCommand import based

from based.langist import language

def to_int(str: str) -> int:
    try:
        return int(str)
    except:
        return None

class use(based):
    """
    This class (command) needs to use anything item on anything target.

    Base: use (SMTH) on (SMTH)

    Classes:

    * __KeyUse() - class needs for use keys on doors in rooms of anything floors in one level and after replace their place on void
        Based use: use [ROOM NAME] on [CORDS]
        Example: use A3 on 0.2.A5
        A3 - name of room in which key laying (because everyone name of rooms is unique).
        0.2.A5 - coordinates of room on whose player want to apply key (0 - number building, 2 - number floor, A5 - name room)

    * __Document_use() - class needs to use, open and read some documents from game level
        Based use: use [doc] in [CORDS] [MODIFY]
        Example: use doc in 0.2.A5 fin
        doc - this arg needs to understand that user want to open, read or use only some document.
        [CORDS] - an arg with cords of document.
        [MODIFY] - arg for understand what use want to do - [read/fin]
    """

    class __Document_use():
        # example use Document: use doc in 0.2.A5
        def __init__(self, command: list[str], level: Level):
            self.command = command
            self.level = level

        def use_doc(self) -> list[str]:
            if (self.command[0] == "use"):
                if (self.command[1] == "doc"):
                    if (self.command[2] == "in"):
                        if ((len(self.command[3].split(".")) == 3) and (to_int(self.command[3].split(".")[0]) and to_int(self.command[3].split(".")[1]) != None)):
                            lst = self.command[3].split(".")
                            for index_building, building in enumerate(self.level.buildings):
                                if (index_building == to_int(lst[0])):
                                    build = building.floors
                                    for index_floor, floor in enumerate(build):
                                        if (index_floor == to_int(lst[1])):
                                            floo = floor.rooms
                                            for room in floo:
                                                if (room.name == lst[2]):
                                                    if (self.command[4] in ["fin", "finish", "f"]):
                                                        for i in range(room.items.__len__()):
                                                            obj = room.items.__getitem__(i)
                                                            req = self.level.generate_finish_requirement()
                                                            if (type(req) == type(obj)):
                                                                if (req.to_dict() == obj.to_dict()):
                                                                    self.level.unlock_all_doors()
                                                                    return language().__getitem__("success_finish_level")
                                                                else:
                                                                    continue
                                                            else:
                                                                continue
                                                        return language().__getitem__("room_not_contains_document_message")
                                                    elif (self.command[4] in ["r", "read", "re"]):
                                                        for i in range(room.items.__len__()):
                                                            obj = room.items.__getitem__(i)
                                                            if (type(Item.Document()) == type(obj)):
                                                                return language().__getitem__("result_reading_min_document_message", {"{name}": f"{obj.name}", "{text}": f"{obj.info}"})
                                                            else:
                                                                continue
                                                        return language().__getitem__("room_not_contains_document_message")
                                                    else:
                                                        return language().__getitem__("incorrect_list_command_argument")
                        else:
                            return language().__getitem__("incorrect_difficulty_for_level_argument")
                    else:
                        return language().__getitem__("incorrect_difficulty_for_level_argument")
                else:
                    return language().__getitem__("incorrect_difficulty_for_level_argument")
            else:
                return language().__getitem__("incorrect_entered_help_ve_command_message")

    class __KeyUse():
        # example use KEY: use A3 on 0.2.A5
        def __init__(self, command: list[str], level: Level):
            self.command = command
            self.level = level

        def __types(self, list: Items, item) -> bool:
            for value in list:
                if (type(value) == type(item)):
                    return True
            return False

        def __remove_key_item(self, room: Room) -> Room:
            types = []
            for item in room.items:
                types.append(type(item))
            if (types.count(type(Item.Key())) > 0):
                index = types.index(type(Item.Key()))
                Items(room.items).remove(room.items[index])
            return room

        def key_on_room_use(self) -> bool:
            if (len(self.command) == 3 and self.command.count(".") == 2):
                cords = self.command[3].split(".")
                for number_build, build in enumerate(self.level.buildings):
                    for number_floor, floor in enumerate(build.floors):
                        for number_room, room in enumerate(floor.rooms):
                            if (room.name.lower() == cords[2].lower()
                            and to_int(cords[0]) == number_build
                            and to_int(cords[1]) == number_floor
                            and self.level.get_names().count(room.name) == 1
                            and self.__types(room.items, Item().Key())
                            and room.blocked == True):
                                room.blocked = False
                                self.level.buildings[number_build].floors[number_floor].rooms[number_room] = room
                                for used_build_number, used_build in enumerate(self.level.buildings):
                                    for used_floor_number, used_floor in enumerate(used_build.floors):
                                        for used_room_number, used_room in enumerate(used_floor.rooms):
                                            if (used_room.name.lower() == self.command[1].lower()):
                                                self.level.buildings[used_build_number].floors[used_floor_number].rooms[used_room_number] = self.__remove_key_item(used_room)
                                            else:
                                                continue
                                self.level.to_json()
                                return True
                            else:
                                continue
                return False
            else:
                return False

    #example command use: use (SMTH) on (SMTH)

    def __init__(self):
        super().__init__()
        pass

    def __is(self, string: str) -> bool:
        if (string.split("")[0] in ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F',
                                           'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
                and string.split("")[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
            return True
        else:
            return False

    def __help_cast(self) -> list[str]:
        if (len(self.arg) >= 2 and self.arg[0] == "use"):
            return None
        else:
            if (len(self.arg) == 1 or self.arg[1] in ["", " "]):
                return language().__getitem__("use_command")

    def cast(self, cl: line) -> list[str]:
        self.arg = cl.command
        res = self.__help_cast()
        if (res is not None):
            return res
        self.Level = cl.Level
        super().cast(cl)
        if (self.__is(self.arg[1]) and self.__KeyUse(self.arg, self.Level).key_on_room_use()):
            return language().__getitem__("success_middle_key_apply_message", {"{arg}": str(self.arg[3]).split(".")[2]})
        elif (len(self.arg) == 4):
            return self.__Document_use(self.arg, self.Level).use_doc()
        else:
            return language().__getitem__("incorrect_typed_command")
