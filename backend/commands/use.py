from backend.funcs.generate_play_space import *
from backend.commands.commandLine import line
from backend.commands.basedCommand import based

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
        Example: use A3 on 0.2.A5
        A3 - name of room in which key laying (because everyone name of rooms is unique
        0.2.A5 - coordinates of room on whose player want to apply key (0 - number building, 2 - number floor, A5 - name room)

    * __Document_use() - class
    """

    class __Document_use():
        # example use Document: use A3 on 0.2.A5
        def __init__(self, command: list[str], level: Level):
            self.command = command
            self.level = level

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
                obj = self.command[3]
                cords = obj.split(".")
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
                                self.level._to_json()
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

    def cast(self, cl: line) -> list[str]:
        self.arg = cl.command
        self.Level = cl.Level
        super().cast(cl)
        message = []
        if (self.__is(self.arg[1]) and self.__KeyUse(self.arg, self.Level).key_on_room_use()):
            return [f"Key was been successfully applied to {str(self.arg[3]).split(".")[2]} room."]
