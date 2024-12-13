
from backend.commands.basedCommand import based
from backend.commands.commandLine import line

class help(based):

    def __init__(self):
        super().__init__()

    def cast(self, cl: line) -> list[str]:
        self.check(cl)
        super().__init__(self.padding, cl)
        if (self.get(0) == "help"):
            f = open("backend/preFiles/app/help_terminal_command", "r")
            file = f.readlines()
            f.close()
            for i in range(len(file)):
                if ("\n" in file[i]):
                    file[i] = file[i].replace("\n", "")
            return file
        else:
            return ["This command can be applied!"]
