import main
from backend.funcs.generate_play_space import _Level, _Item, _Items, _Room
from main import LEVEL


class use():

    Level = _Level([])

    class __Finish_Game(_Level):
        # example use Document: use A3 on 0.2.A5
        def __init__(self, command: list[str]):
            super().__init__(LEVEL)
            self.command = command
            self.level = Level

    class __KeyUse(_Level):
        # example use KEY: use A3 on 0.2.A5
        def __init__(self, command: list[str]):
            super().__init__(LEVEL)
            self.command = command
            self.level = Level

        def __to_int(self, str: str) -> int:
            try:
                return int(str)
            except:
                return None

        def __types(self, list: _Items, item) -> bool:
            for value in list:
                if (type(value) == type(item)):
                    return True
            return False

        def __remove_key_item(self, room: _Room) -> _Room:
            types = []
            for item in room.items:
                types.append(type(item))
            if (types.count(type(_Item.Key())) > 0):
                index = types.index(type(_Item.Key()))
                _Items(room.items).remove(room.items[index])
            return room

        def key_on_room_use(self) -> bool:
            if (len(self.command) == 3 and self.command.count(".") == 2):
                obj = self.command[3]
                cords = obj.split(".")
                for number_build, build in enumerate(self.level.buildings):
                    for number_floor, floor in enumerate(build.floors):
                        for number_room, room in enumerate(floor.rooms):
                            if (room.name.lower() == cords[2].lower()
                            and self.__to_int(cords[0]) == number_build
                            and self.__to_int(cords[1]) == number_floor
                            and self.level.get_names().count(room.name) == 1
                            and self.__types(room.items, _Item().Key())
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
                                main.LEVEL = self.level
                                self.level._to_json()
                                return True
                            else:
                                continue
                return False
            else:
                return False


    #example command use: use (SMTH) on (SMTH)

    def __init__(self, arg, level: _Level):
        global Level
        self.arg = arg
        self.level = level
        Level = level

    def __is(self, string: str) -> bool:
        if (string.split("")[0] in ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F',
                                           'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
                and string.split("")[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
            return True
        else:
            return False

    def __to_int(self, str: str) -> int:
        try:
            return int(str)
        except:
            return None

    def cast(self) -> list:
        message = []
        if (self.arg == list):
            self.arg = list(self.arg)
            if (self.__is(self.arg[1]) and self.__KeyUse(self.arg).key_on_room_use()):
                return [f"Key was been successfully applied to {str(self.arg[3]).split(".")[2]} room."]
