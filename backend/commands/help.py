
from backend.commands.basedCommand import based
from backend.commands.commandLine import line
from based.langist import language


class help(based):

    def __init__(self):
        super().__init__()

    def cast(self, cl: line) -> list[str]:
        self.check(cl)
        super().__init__(self.padding, cl)
        if (self.get(0) == "help"):
            return language().__getitem__("help_terminal_command")
        else:
            return language().__getitem__("cant_applied_command")
