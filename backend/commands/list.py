import builtins
from types import NoneType

from backend.commands.basedCommand import based as BASE
from backend.commands.commandLine import line as LINE
import based.gate
from backend.funcs.generate_play_space import Items, Item
from based.Logger import stack
from based.langist import language


class list(BASE):

    def __to_int(self, str: str) -> int:
        try:
            return int(str)
        except:
            return None

    def __is(self, what: str) -> bool:
        if (what.lower() == "room"):
            if (str(self.arg[1])[0] in ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F',
                                               'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
                    and str(self.arg[1])[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                return True
            else:
                return False
        elif (what.lower() == "floor"):
            if (len(builtins.list(self.arg)) == 3
            and builtins.list(self.arg)[1] == "floor"
            and self.__to_int(self.arg[2]) is not None):  # example: list(D) floor 0              D - don't send in arg
                return True
            else:
                return False
        elif (what.lower() == "build"):
            if (len(builtins.list(self.arg)) == 3
            and builtins.list(self.arg)[1] == "build"
            and self.__to_int(self.arg[2]) is not None):  # example: list(D) build 0              D - don't send in arg
                return True
            else:
                return False
        else:
            return False

    def cast(self, line: LINE) -> builtins.list:

        def lget(d: dict) -> str:
            for key in d.keys():
                return key

        self.arg = line.command
        self.Level = line.Level
        message = []
        if len(line.command) == 1 or (len(line.command) == 2 and line.command[1] in ["", " ", None]):
            return language().__getitem__("list_command")
        if (self.__is("room")):
            for build in self.Level.buildings:
                for floor in build.floors:
                    for room in floor.rooms:
                        if (str(room.name).lower() == str(self.arg[1]).lower()):
                            if (room.blocked == False):
                                if (room.items.__len__() == 0):
                                    return language().__getitem__("room_list_items_empty_message")
                                else:
                                    for i in range(room.items.__len__()):
                                        obj = dict(room.items.__getitem__(i))
                                        message.append(lget(obj))
                                    return message
                            else:
                                return language().__getitem__("cant_send_list_items_because_room_is_blocked")
                        else:
                            continue
            return language().__getitem__("incorrect_room_name")
        elif (self.__is("floor")):
            now_building = str(stack().get_stack().get("now_building"))
            if (now_building not in [None, "None"]):
                for number, build in enumerate(self.Level.buildings):
                    if (number == int(str(now_building))):
                        for number, floor in enumerate(build.floors):
                            if (number == self.__to_int(builtins.list(str(self.arg))[1])):
                                for room in floor.rooms:
                                    message.append(room.name)
                                return message
                            else:
                                continue
                return language().__getitem__("incorrect_floor_number")
            else:
                based.gate.Logger().log("Stack don't have a now building argument that his was been set to standard zero.")
                build = self.Level.buildings[0]
                for number, floor in enumerate(build.floors):
                    if (number == self.__to_int(builtins.list(self.arg)[2])):
                        for room in floor.rooms:
                            message.append(room.name)
                        return message
                    else:
                        continue
                return language().__getitem__("incorrect_floor_number")
        elif (self.__is("build")):
            if (self.__to_int(str(builtins.list(str(self.arg))[1]))):
                stack().controller({"now_building": str(builtins.list(str(self.arg))[1])})
                return language().__getitem__("setting_building_message", {"build": str(builtins.list(str(self.arg))[1])})
            else:
                return language().__getitem__("incorrect_building_number")
        else:
            based.gate.Logger().log(f"Invalid command operation with \"list\" command. Command: {str(self.arg)}")
            return language().__getitem__("incorrect_list_command_argument")
