
from backend.commands.basedCommand import based
from backend.commands.commandLine import line

class help(based):

    def __init__(self, from_t: bool = False):
        self.from_t = from_t
        super().__init__()

    def cast(self, cl: line) -> list[str]:
        if (self.from_t == False):
            if (cl.command[0] == "help"):
                f = open(f"backend/preFiles/app/help_message", "r")
                message = f.readlines()
                f.close()
                for i in range(len(message)):
                    if ("\n" in message[i]):
                        message[i] = message[i].replace("\n", "")
                return message
            else:
                return ["Entered command is not correct!"]
        else:
            if (cl.command[1] == "help"):
                f = open(f"backend/preFiles/app/help_message", "r")
                message = f.readlines()
                f.close()
                for i in range(len(message)):
                    if ("\n" in message[i]):
                        message[i] = message[i].replace("\n", "")
                return message
            else:
                return ["Entered command is not correct!"]
