
from backend.commands.basedCommand import based
from backend.commands.commandLine import line

from backend.ve_commands.create import create
from backend.ve_commands.help import help
from backend.ve_commands.start import start
from backend.commands.clear import clear
from backend.commands.delete import delete
from backend.ve_commands.change import change
from backend.ve_commands.set import set

class ve_gate(based):

    def __init__(self):
        super().__init__()

    def __get_command_catalogue(self) -> dict[str, based]:
        catalogue = {
            "help": help(),
            "create": create(),
            "c": clear(),
            "clear": clear(),
            "start": start(),
            "del": delete(),
            "delete": delete(),
            "ch": change(),
            "change": change(),
            "set": set()
        }
        return catalogue

    def cast(self, cl: line) -> list[str]:
        self.check(cl)
        super().__init__(self.padding, cl)
        if (self.__get_command_catalogue().get(cl.command[1]) != None):
            return self.__get_command_catalogue().get(cl.command[1]).cast(line(cl.command, cl.Level))
        else:
            return ["This command can't be applied."]