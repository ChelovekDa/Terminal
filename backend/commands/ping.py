import backend
from backend.commands.basedCommand import based

class ping(based):
    """
    This class (command) needs to ping anything item in whole level.

    Base using command in terminal: ping (SMTH)

    NOTE: Player can't use this command for Key items before as 10 minutes have passed after started game.
    (This has been done because player can abuse this command and learn all places with keys)
    """

    def __init__(self):
        super().__init__()
        pass

    def __listed(self) -> list[str]:
        return backend.funcs.generate_play_space.Item().get_list_items()

    def __contains__(self, item: str) -> bool:
        if (len(item) >= 6):
            line = item.split(" ")
            return line[0] == "ping" and line[1] in self.__listed()
        return False

    def __str(self, obj: list[str]) -> str:
        das = ""
        for item in obj:
            das = f"{das} {str(item)}"
        return das

    #Example: ping (SMTH)
    def cast(self, line: backend.commands.commandLine) -> list[str]:
        super().cast(line)
        self.command = self.__str(line.command)
        self.Level = line.Level
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