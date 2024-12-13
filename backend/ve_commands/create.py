import os
import threading

from backend.commands.basedCommand import based
from backend.commands.commandLine import line
from backend.funcs.generate_play_space import Generate
from based.Logger import Logger, stack

from backend.funcs.generate_play_space import Level
from based.based_values import values

import tkinter.messagebox

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
    def __check(name) -> bool:
        lst = os.listdir(f"{values().get_base_directory()}/Terminal/Levels")
        for item in lst:
            if (item == f"{name}.json"):
                if (len(lst) > 300):
                    th = threading.Thread(
                        target=lambda: tkinter.messagebox.showinfo(title="Info",
                                                                   message="You have too much saved levels. For optimized work of the Terminal you can delete a part of them."), daemon=True)
                    th.start()
                return True
        del lst
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
        self.cl = line([], [])
        super().__init__()

    def help(self) -> list[str]:
        f = open("backend/preFiles/app/create_message", "r")
        message = f.readlines()
        f.close()
        for i in range(len(message)):
            if ("\n" in message[i]):
                message[i] = message[i].replace("\n", "")
        return message

    def cast(self, cl: line) -> list[str]:
        message = []
        self.check(cl)
        super().__init__(self.padding, cl)

        if (self.get(0) == "create"):
            if (self.__len__() == 1):
                return self.help()
            elif (self.__len__() == 2 or (self.__len__() == 3 and self.get(2) == "-y")):
                if (self.get(1) == "l"):
                    level = Generate(name=Level([]).gen_name()).generate()
                    stack().controller({values().get_base_stack_for_last_level_created_name(): {level.name}})
                    del level
                    return ["Level was been success created!"]
                elif (self.get(1) == " "):
                    message = self.help()
                    message.insert(0, "This level-name is not be setting!")
                    return message
                else:
                    if (self.__check(self.get(1))):
                        return ["Level with this name already exists."]
                    try:
                        level = Generate(name=self.get(1)).generate()
                        stack().controller({values().get_base_stack_for_last_level_created_name(): {level.name}})
                        del level
                        return ["Level was been success created!"]
                    except Exception as e:
                        Logger().log(
                            f"When creating level with custom user's name that was appeared a error. Custom name: <{self.get(1)}>. Full command: <{cl.command}>. Error that was appeared: {e}")
                        return ["Level with this custom name not can't be created."]

            elif (self.__len__() == 3):
                if (self.__to_int(self.get(2)) or self.__contains(int(self.get(2)))):
                    if (self.__check(self.get(1))):
                        return ["Level with this name already exists."]
                    Logger().log("Creating new level with custom difficulty..")
                    level = Generate(difficulty=int(self.get(2)), name=self.get(1)).generate()
                    stack().controller({values().get_base_stack_for_last_level_created_name(): {level.name}})
                    del level
                    Logger().log("Creating complete!")
                    return [f"Creating level with custom difficulty {self.get(2)} was complete!"]
                else:
                    Logger().log(
                        f"Cant create new level with custom difficulty because need args was not be found. Command: <{cl.command}>.")
                    message = ["The need arguments was not be found!"]
        else:
            return ["This not command!"]

        return message
