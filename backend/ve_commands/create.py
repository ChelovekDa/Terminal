import os
import threading

from backend.commands.basedCommand import based
from backend.commands.commandLine import line
from backend.funcs.generate_play_space import Generate
from based.Logger import Logger, stack

from backend.funcs.generate_play_space import Level
from based.based_values import values

import tkinter.messagebox

from based.langist import language


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
                                                                   message=language().__getitem__("optimized_create_tkinter_message")[0]), daemon=True)
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
        return language().__getitem__("create_command")

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
                    return language().__getitem__("success_new_level_creating")
                elif (self.get(1) == " "):
                    message = self.help()
                    message.insert(0, language().__getitem__("incorrect_level_name_for_creating")[0])
                    return message
                else:
                    if (self.__check(self.get(1))):
                        return language().__getitem__("already_exists_level_message")
                    try:
                        level = Generate(name=self.get(1)).generate()
                        stack().controller({values().get_base_stack_for_last_level_created_name(): {level.name}})
                        del level
                        return language().__getitem__("success_new_level_creating")
                    except Exception as e:
                        Logger().log(
                            f"When creating level with custom user's name that was appeared a error. Custom name: <{self.get(1)}>. Full command: <{cl.command}>. Error that was appeared: {e}")
                        return language().__getitem__("error_creating_level_with_custom_name_message")

            elif (self.__len__() == 3):
                if (self.__to_int(self.get(2)) or self.__contains(int(self.get(2)))):
                    if (self.__check(self.get(1))):
                        return language().__getitem__("already_exists_level_message")
                    Logger().log("Creating new level with custom difficulty..")
                    level = Generate(difficulty=int(self.get(2)), name=self.get(1)).generate()
                    stack().controller({values().get_base_stack_for_last_level_created_name(): {level.name}})
                    del level
                    Logger().log("Creating complete!")
                    return language().__getitem__("success_creating_level_with_custom_difficulty_message", {"diff": self.get(2)})
                else:
                    Logger().log(
                        f"Cant create new level with custom difficulty because need args was not be found. Command: <{cl.command}>.")
                    return language().__getitem__("incorrect_difficulty_for_level_argument")
        else:
            return language().__getitem__("cant_applied_command")

        return message
