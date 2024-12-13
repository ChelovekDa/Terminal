import backend
from backend.commands.basedCommand import based
from based.Logger import stack
from based.based_values import values
from backend.commands.commandLine import line


class ping(based):
    """
    This class (command) needs to ping anything item in whole level.

    Base using command in terminal: ping (SMTH)

    NOTE: Player can't use this command for Key items before as 10 minutes have passed after started game.
    (This has been done because player can abuse this command and learn all places with keys)
    """

    def __init__(self):
        self.cl = line([], None)
        super().__init__()
        pass

    def __listed(self) -> list[str]:
        return backend.funcs.generate_play_space.Item().get_list_items()

    def __contains__(self, item: str) -> bool:
        if (len(item) >= 6):
            line = item.split(" ")
            return line[0] == "ping" and line[1] in self.__listed()
        return False

    def __check(self) -> bool:
        return int(stack().get_stack().get(values().get_base_game_time_stack())) >= 600

    def __str(self, obj: list[str]) -> str:
        das = ""
        for item in obj:
            das = f"{das} {str(item)}"
        return das

    def __help_cast(self) -> list[str]:
        if (len(self.cl.command) == 2 and self.cl.command[0] == "ping"):
            return None
        else:
            if (len(self.cl.command) == 1 or self.cl.command[1] in ["", " "]):
                f = open("backend/preFiles/app/ping_command_help", "r")
                file = f.readlines()
                f.close()
                for i in range(len(file)):
                    if ("\n" in file[i]):
                        file[i] = file[i].replace("\n", "")
                return file


    #Example: ping (SMTH)
    def cast(self, cl: line) -> list[str]:
        self.check(cl)
        super().__init__(self.padding, cl)
        res = self.__help_cast()
        if (res is not None):
            return res
        if (not self.__check()):
            return ["This command can be applied when from the beginning of start game passed 10 minutes."]
        self.command = self.__str(cl.command)
        self.Level = cl.Level
        message = []
        if (self.__contains__(self.command)):
            if (self.command.count(";") > 0):
                self.command = self.command.replace(";", "")
            line = self.command.split(" ")

            for building in self.Level.buildings:
                for floor in building.floors:
                    for room in floor.rooms:
                        if (line[1].lower() in room.items.__liter__()):
                            message.append(f"Was been found this item in \"{room.name}\" room!")

        if (not self.__contains__(self.command)):
            return ["Command was been entered not correct!"]
        elif (len(message) == 0):
            return ["This item wasn't found!"]

        return message