
import os
import json
import time

from backend.commands.commandLine import line
from backend.commands.basedCommand import based
from based.Logger import Logger
from based.based_values import values
from frontend.Menu.root import MENUs as MENU

from backend.commands.clear import clear

class start(based):
    """
    In this command happens all backend operations for start game.
    """

    def __init__(self, from_t: bool = False):
        self.from_t = from_t
        super().__init__()

    def cast(self, cl: line) -> list[str]:
        message = []

        if (self.from_t == False):
            if (cl.command[0] == "start"):
                if (len(cl.command) == 1):
                    f = open("backend/preFiles/app/start_message", "r")
                    message = f.readlines()
                    f.close()
                    for i in range(len(message)):
                        if ("\n" in message[i]):
                            message[i] = message[i].replace("\n", "")
                    return message
                elif (len(cl.command) == 2):
                    if (cl.command[1] in ["", " ", "l"]):
                        MENU.get_root().destroy()
                        return []
                    else:
                        for item in list(os.listdir(f"{values().get_base_directory()}/Terminal/Levels")):
                            if (item.split(".")[0] == cl.command[1]):
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
                                time.sleep(1)
                                MENU.get_root().destroy()
                                return []
                            else:
                                continue
                else:
                    message = ["This command can't be applied."]
            else:
                message = ["This is not command"]
        else:
            if (cl.command[1] == "start"):
                if (len(cl.command) == 2):
                    f = open("backend/preFiles/app/start_message", "r")
                    message = f.readlines()
                    f.close()
                    for i in range(len(message)):
                        if ("\n" in message[i]):
                            message[i] = message[i].replace("\n", "")
                    return message
                elif (len(cl.command) == 3):
                    if (cl.command[2] in ["", " ", "l"]):
                        return ["This level already started!"]
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
                                time.sleep(1)
                                return ["Success change to other level."]
                            else:
                                continue
                else:
                    message = ["This command can't be applied."]
            else:
                message = ["This is not command"]

        return message