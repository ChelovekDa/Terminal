import os
import json
import time

from backend.commands.commandLine import line
from backend.commands.basedCommand import based
from based.Logger import Logger, stack
from based.based_values import values

from backend.commands.clear import clear
from backend.commands.delete import delete
from based.langist import language


class start(based):
    """
    In this command happens all backend operations for start game.
    """

    def __replace(self) -> None:
        """
        Replaced all elements in app window.
        """
        delete().other_cast()
        stack().controller({"from_terminal": "True"})
        Logger().log("Changed window to the Terminal console..")

    def help(self) -> list[str]:
        return language().__getitem__("start_command")

    def cast(self, cl: line) -> list[str]:
        self.check(cl)
        super().__init__(self.padding, cl)
        if (self.padding == 0):
            if (cl.command[0] == "start"):
                if (self.__len__() == 1):
                    return self.help()
                elif (len(cl.command) == 2):
                    if (cl.command[1] in ["", " ", "l"]):
                        self.__replace()
                        return []
                    else:
                        if len(list(os.listdir(f"{values().get_base_directory()}/Terminal/Levels"))) == 0:
                            return language().__getitem__("cant_applied_command")
                        for item in list(os.listdir(f"{values().get_base_directory()}/Terminal/Levels")):
                            if (item.split(".")[0] == self.get(1)):
                                with open(f"{values().get_base_directory()}/Terminal/Levels/{item}", "r") as read_file:
                                    data = json.load(read_file)
                                data = dict(data)
                                Logger().log(
                                    f"Write to activate.json a new active level by site: <{values().get_base_directory()}/Terminal/Levels/{item}>")
                                open(f"backend/preFiles/app/activate.json", "w").close()
                                with open(f"backend/preFiles/app/activate.json", "w") as write_file:
                                    json.dump(data, write_file)
                                del data
                                Logger().log("Write is success complete.")
                                self.__replace()
                                return []
                            else:
                                continue
                        else:
                            return language().__getitem__("cant_applied_command")
                else:
                    return language().__getitem__("cant_applied_command")
            else:
                return language().__getitem__("cant_applied_command")
        else:
            if (cl.command[1] == "start"):
                if (len(cl.command) == 2):
                    return self.help()
                elif (len(cl.command) == 3):
                    if (cl.command[2] in ["", " ", "l"]):
                        return language().__getitem__("already_started_level_error_message")
                    else:
                        for item in list(os.listdir(f"{values().get_base_directory()}/Terminal/Levels")):
                            if (item.split(".")[0] == cl.command[2]):
                                with open(f"{values().get_base_directory()}/Terminal/Levels/{item}", "r") as read_file:
                                    data = json.load(read_file)
                                data = dict(data)
                                Logger().log(
                                    f"Write to activate.json a new active level by site: <{values().get_base_directory()}/Terminal/Levels/{item}>")
                                open(f"backend/preFiles/app/activate.json", "w").close()
                                with open(f"backend/preFiles/app/activate.json", "w") as write_file:
                                    json.dump(data, write_file)
                                del data
                                Logger().log("Write is success complete.")
                                clear().cast(cl)
                                time.sleep(0.2)
                                return language().__getitem__("success_changed_to_other_level_message")
                            else:
                                continue
                else:
                    return language().__getitem__("cant_applied_command")
            else:
                return language().__getitem__("cant_applied_command")

        return []