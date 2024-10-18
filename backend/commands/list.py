import builtins
from based.gate import Gate, Logger

from main import LEVEL

class list():

    def __is(self, what: str) -> bool:
        if (what.lower() == "room"):
            if (str(self.arg).split("")[0] in ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F',
                                               'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
                    and str(self.arg).split("")[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                return True
            else:
                return False
        elif (what.lower() == "floor"):
            if (len(builtins.list(str(self.arg))) == 2 and builtins.list(str(self.arg))[
                0] == "floor"):  # example: list(D) floor 0              D - don't send in arg
                return True
            else:
                return False
        elif (what.lower() == "build"):
            if (len(builtins.list(str(self.arg))) == 2 and builtins.list(str(self.arg))[
                0] == "build"):  # example: list(D) build 0              D - don't send in arg
                return True
            else:
                return False
        else:
            return False

    def __to_int(self, str: str) -> int:
        try:
            return int(str)
        except:
            return None

    def __init__(self, arg):
        self.arg = arg

    def cast(self) -> builtins.list:
        message = []
        if (self.__is("room")):
            for build in LEVEL.buildings:
                for floor in build.floors:
                    for room in floor.rooms:
                        if (room.name.lower() == str(self.arg).lower()):
                            if (room.blocked == False):
                                return room.items
                            else:
                                return ["This room is blocked!", "First unlocked the room with help the key."]
                        else:
                            continue
            return ["Invalid room name"]
        elif (self.__is("floor")):
            now_building = Gate().stack().get_stack().get("now_building")
            if (now_building != "None" or None):
                for number, build in enumerate(LEVEL.buildings):
                    if (number == int(now_building)):
                        for number, floor in enumerate(build.floors):
                            if (number == self.__to_int(builtins.list(str(self.arg))[1])):
                                for room in floor.rooms:
                                    message.append(room.name)
                                return message
                            else:
                                continue
                return ["Invalid floor number"]
            else:
                Logger().log("Stack don't have a now building argument that his was been set to standard zero.")
                build = LEVEL.buildings[0]
                for number, floor in enumerate(build.floors):
                    if (number == self.__to_int(builtins.list(str(self.arg))[1])):
                        for room in floor.rooms:
                            message.append(room.name)
                        return message
                    else:
                        continue
                return ["Invalid floor number"]
        elif (self.__is("build")):
            if (self.__to_int(str(builtins.list(str(self.arg))[1]))):
                Gate().stack().controller({"now_building": str(builtins.list(str(self.arg))[1])})
                return [f"The looked building was been set to \"{str(builtins.list(str(self.arg))[1])}\"!",
                        "For look the floor write \"list floor\" and number floor that you want to see."]
            else:
                return ["Invalid building number"]
        else:
            Logger().log(f"Invalid command operation with \"list\" command. Command: {str(self.arg)}")
            return ["Invalid command operation"]







