
from backend.commands.basedCommand import based
from backend.commands.commandLine import line
from backend.funcs.generate_play_space import Generate
from based.Logger import Logger

from backend.funcs.generate_play_space import Level

class create(based):
    """
    Command <create> needs to create something items in Virtual Environment (VE), then not be owns to common Terminal.
    Based example to use: create [SMTH]

    Examples to use this command (all kinds):
        BASED:
            * create [NOTHING] - printed help for <create> command

        CREATE LEVEL:
            * create [l] - creating new level and using his in the future game
            * create [new_level (OR SMTH NAME)] - creating new level and using his in the future game, but his name - this arg

    cl: Based param for cast() func with command lines (list) and Level's object
    :return: Message that will be printed on the Terminal's console

    NOTE: for more information see documentation file of this command
    """

    @staticmethod
    def __to_int(string: str) -> bool:
        try:
            return type(int(string)) == int
        except:
            return False

    @staticmethod
    def __contains(item: int) -> bool:
        catalogue = {
            1: "easy",
            2: "medium",
            3: "hard"
        }
        return catalogue.__contains__(item)

    def __init__(self, from_t: bool = False):
        self.from_T = from_t
        super().__init__()

    def __from_ve(self, cl: line) -> list[str]:
        message = []
        if (cl.command[0] == "create"):
            if (len(cl.command) == 1):
                f = open("backend/preFiles/app/create_message", "r")
                message = f.readlines()
                f.close()
                for i in range(len(message)):
                    if ("\n" in message[i]):
                        message[i] = message[i].replace("\n", "")

            elif (len(cl.command) == 2):
                if (cl.command[1] == "" or " "):
                    f = open("backend/preFiles/app/create_message", "r")
                    message = f.readlines()
                    f.close()
                    for i in range(len(message)):
                        if ("\n" in message[i]):
                            message[i] = message[i].replace("\n", "")
                    message.insert(0, "This level-name is not be setting!")
                elif (cl.command[1] == "l"):
                    level = Generate(name=Level([]).gen_name()).generate()
                    level.to_json()
                    message = ["Level was been success created!"]
                    del level
                else:
                    try:
                        level = Generate(name=cl.command[1]).generate()
                        level.to_json()
                        message = ["Level was been success created!"]
                        del level
                    except:
                        Logger().log(
                            f"When creating level with custom user name that was appeared a error. Custom name: <{cl.command[1]}>. Full command: <{cl.command}>")
                        message = ["Level with this custom name not can't be created."]

            elif (len(cl.command) == 3):
                if (self.__to_int(cl.command[2]) or self.__contains(int(cl.command[2]))):
                    Logger().log("Creating new level with custom difficulty..")
                    level = Generate(difficulty=int(cl.command[2]), name=cl.command[1]).generate()
                    level.to_json()
                    del level
                    Logger().log("Creating complete!")
                    message = [f"Creating level with custom difficulty {cl.command[2]} was complete!"]
                else:
                    Logger().log(
                        f"Cant create new level with custom difficulty because need args was not be found. Command: <{cl.command}>.")
                    message = ["The need arguments was not be found!"]
        else:
            return ["This not command!"]
        return message

    def __from_terminal(self, cl: line) -> list[str]:
        message = []
        #ve create ...
        if (cl.command[1] == "create"):
            if (len(cl.command) == 2):
                f = open("backend/preFiles/app/create_message", "r")
                message = f.readlines()
                f.close()
                for i in range(len(message)):
                    if ("\n" in message[i]):
                        message[i] = message[i].replace("\n", "")

            elif (len(cl.command) == 3):
                if (cl.command[2] == "" or " "):
                    f = open("backend/preFiles/app/create_message", "r")
                    message = f.readlines()
                    f.close()
                    for i in range(len(message)):
                        if ("\n" in message[i]):
                            message[i] = message[i].replace("\n", "")
                    message.insert(0, "This level-name is not be setting!")
                elif (cl.command[2] == "l"):
                    level = Generate(name=Level([]).gen_name()).generate()
                    level.to_json()
                    message = ["Level was been success created!"]
                    del level
                else:
                    try:
                        level = Generate(name=cl.command[2]).generate()
                        level.to_json()
                        message = ["Level was been success created!"]
                        del level
                    except:
                        Logger().log(f"When creating level with custom user name that was appeared a error. Custom name: <{cl.command[2]}>. Full command: <{cl.command}>")
                        message = ["Level with this custom name not can't be created."]

            elif (len(cl.command) == 4):
                if (self.__to_int(cl.command[3]) or self.__contains(int(cl.command[3]))):
                    Logger().log("Creating new level with custom difficulty..")
                    level = Generate(difficulty=int(cl.command[3]), name=cl.command[2]).generate()
                    level.to_json()
                    del level
                    Logger().log("Creating complete!")
                    message = [f"Creating level with custom difficulty {cl.command[2]} was complete!"]
                else:
                    Logger().log(
                        f"Cant create new level with custom difficulty because need args was not be found. Command: <{cl.command}>.")
                    message = ["The need arguments was not be found!"]
        else:
            return ["This not command!"]
        return message

    def cast(self, cl: line) -> list[str]:
        message = []

        if (self.from_T == False):
            message = self.__from_ve(cl)
        else:
            message = self.__from_terminal(cl)

        return message



