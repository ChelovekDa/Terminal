
from backend.commands.basedCommand import based
from backend.commands.commandLine import line

class help(based):

    def cast(self, cl: line) -> list[str]:
        self.check(cl)
        super().__init__(self.padding, cl)
        if (self.get(0) == "help"):
            f = open(f"backend/preFiles/app/help_message", "r")
            message = f.readlines()
            f.close()
            for i in range(len(message)):
                if ("\n" in message[i]):
                    message[i] = message[i].replace("\n", "")
            return message
        else:
            return ["Entered command is not correct!"]
