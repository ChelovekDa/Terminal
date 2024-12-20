import time
import tkinter
import os

import requests
import json

import frontend.Game.window
from backend.commands.basedCommand import based
from backend.commands.ping import ping
from backend.commands.help import help as help_t
from backend.commands.use import use
from backend.commands.clear import clear
from backend.commands.list import list as lst
from backend.commands.commandLine import line
from backend.commands.delete import delete

from backend.ve_commands.ve_gate import ve_gate
from backend.ve_commands.help import help
from backend.ve_commands.create import create
from backend.ve_commands.start import start
from backend.ve_commands.change import change
from backend.ve_commands.set import set
from based.langist import language

from frontend.Game.window import Tk
from backend.funcs.generate_play_space import Level as Level, Building, Floor, Room, _based
from based.based_values import values
from based.Logger import Logger, stack

class Gate():
    """
    This main class for all FUNCs.
    Gate - class with all methods for app.
    main.py - main class of all APP.

    Classes:
    * stack() - class for manage and use the stack file.
    * Game() - main class for game manage.
    """

    class Game():
        """
        Subclasses:
        * cmd() - class for manage terminal's entry and printed text on terminal screen.
        * VE() - class for manage terminal's menu
        """

        LEVEL = Level

        def __init__(self, level: Level):
            global LEVEL
            LEVEL = level

        class cmd():

            def __init__(self, terminal_root: Tk):
                self.root = terminal_root
                self.special = ["clear", "c", "delete", "del"]

            def update_terminal_text(self, new_text: list[str], username: str = values().get_base_username(), replace: bool = False) -> Tk:
                """
                This function needs to update text on user Terminal when him playing and adding new information.

                :argument new_text - text that you want to print to user screen.
                :argument replace - are you want to delete all information on terminal screen and replace it?
                """

                if (replace):
                    self.root.listbox.delete(0, tkinter.END)
                    self.root.listbox.insert(0, "")
                    if (username == "|"):
                        for i in range(len(new_text)):
                            self.root.listbox.insert(i + 1, f"  {new_text[i]}")
                    else:
                        for i in range(len(new_text)):
                            self.root.listbox.insert(i + 1, f"  <{username}>: {new_text[i]}")
                else:
                    #remove empty lines
                    for i in range(self.root.listbox.size()):
                        if (i == 0):
                            continue
                        res = str(self.root.listbox.get(i, i))
                        if (res not in ["", "('s',)", "('',)", "('\\t',)"]):
                            continue
                        else:
                            if (str(self.root.listbox.get(i+1, i+1)) in ["", "('s',)", "('',)", "('\\t',)"]
                            and str(self.root.listbox.get(i+2, i+2)) in ["", "('s',)", "('',)", "('\\t',)"]):
                                self.root.listbox.delete(i, tkinter.END)
                                break
                            else:
                                continue

                    if (username == "|"):
                        index = self.root.listbox.size()
                        for line in new_text:
                            self.root.listbox.insert(index, f"  {line}")
                            index += 1
                    else:
                        index = self.root.listbox.size()
                        for line in new_text:
                            self.root.listbox.insert(index, f"  <{username}>: {line}")
                            index+=1

                index = self.root.listbox.size()
                for i in range(31):
                    self.root.listbox.insert(index, "\t")
                    index += 1
                return self.root

            def __get_command_catalogue(self) -> dict[str, based]:
                catalogue = {
                    "ve": ve_gate(),
                    "VE": ve_gate(),
                    "help": help_t(),
                    "ping": ping(),
                    "use": use(),
                    "c": clear(),
                    "clear": clear(),
                    "list": lst(),
                    "del": delete(),
                    "delete": delete()
                }
                return catalogue

            def _convert(self, command_arg: str) -> list[str]:
                lst = []
                bases = ["\n\n\n\n\n\n\n\n\n\n", "\n\n\n\n\n\n\n\n\n", "\n\n\n\n\n\n\n\n", "\n\n\n\n\n\n\n", "\n\n\n\n\n\n", "\n\n\n\n\n", "\n\n\n\n", "\n\n\n", "\n\n", "\n"]
                if (command_arg.count("\n") > 0):
                    for obj in bases:
                        if (obj in command_arg):
                            command_arg = command_arg.replace(obj, ";")
                if (command_arg.count(";") > 1):
                    lst = command_arg.split(";")
                    for i, line in enumerate(lst):
                        if (line.count(" ") >= 1):
                            lst[i] = line.split(" ")
                else:
                    lst = str(command_arg.replace(";", "")).split(" ")

                return lst

            def activate_command(self) -> str:
                """
                This function need to do the commands from terminal that user entered.
                command - this parameter contains a list with all command lines that user entered.
                """

                das = str(self.root.entry.get("1.0", tkinter.END))
                self.update_terminal_text([f"{das}"])
                command = self._convert(das)
                del das

                username = values().get_base_terminal_system_username()
                if (self.__get_command_catalogue().get(command[0]) == None):
                    self.update_terminal_text(language().__getitem__("cant_apply_command_gate_message"), username=username)
                    self.update_terminal_text([], username="|")
                    Logger().log(f"Command <{str(command)}> is not be found.")

                else:
                    if (len(command) >= 1 and command[0] in self.special):
                        self.update_terminal_text(self.__get_command_catalogue().get(command[0]).cast(line(command, LEVEL)), username="|")
                        Logger().log(f"Was been applied command <{str(command)}>")

                    elif (len(command) == 1 and self.__get_command_catalogue().get(command[0]) != None):
                        self.update_terminal_text(self.__get_command_catalogue().get(command[0]).cast(line(command, LEVEL)), username=username)
                        Logger().log(f"Was been applied command <{str(command)}>")

                    elif (len(command) >= 2 and command[1] != "") or (len(command) == 1 and command[0] in ["VE", "ve"]):
                        self.update_terminal_text(self.__get_command_catalogue().get(command[0]).cast(line(command, LEVEL)), username=username)
                        Logger().log(f"Was been applied command <{str(command)}>")

                    else:
                        Logger().log(f"Command <{str(command)}> cant be applied.")
                        self.update_terminal_text(language().__getitem__("less_length_than_need_gate_message"), username=username)
                res = ""
                for item in command:
                    res = res + f" {item}"
                return res

        class VE(cmd):

            def __init__(self, terminal_root: Tk):
                super().__init__(terminal_root)

            def __convert(self, command_arg: str) -> list[str]:
                return super()._convert(command_arg)

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
                
            def activate_command(self) -> str:
                """
                For more details see parent func.
                """

                das = str(self.root.entry.get("1.0", tkinter.END))
                self.update_terminal_text([f"{das}"])
                command = self.__convert(das)
                del das

                username = values().get_base_terminal_system_username()
                if (self.__get_command_catalogue().get(command[0]) == None):
                    self.update_terminal_text(language().__getitem__("cant_apply_command_gate_message"), username=username)
                    self.update_terminal_text([], username="|")
                    Logger().log(f"Command <{str(command)}> is not be found.")
                else:
                    if (len(command) >= 1):
                        if (command[0] in self.special):
                            self.update_terminal_text(self.__get_command_catalogue().get(command[0]).cast(line(command, LEVEL)), username="|")
                            Logger().log(f"Was been applied command <{str(command)}>")
                        else:
                            self.update_terminal_text(self.__get_command_catalogue().get(command[0]).cast(line(command, LEVEL)), username=username)
                            Logger().log(f"Was been applied command <{str(command)}>")
                    else:
                        Logger().log(f"Command <{str(command)}> cant be applied.")
                        self.update_terminal_text(language().__getitem__("less_length_than_need_gate_message"), username=username)
                res = ""
                for index, item in enumerate(command):
                    if index == 0:
                        res = str(item)
                    else:
                        res = res + f" {item}"
                return res

    def clear(self, password: str) -> None:
        """This function need to clear all program files."""
        if (stack().clear(password)):
            open("backend/prefiles/app/activate.json", "w+").close()
        return None

    def counter(self):
        count = 0
        while True:
            count+=1
            stack().controller({values().get_base_game_time_stack(): count})
            time.sleep(1)

    def check(self) -> bool:
        if (os.path.exists(f"{values().get_base_directory()}/Terminal")):
            if (os.path.exists(f"{values().get_base_directory()}/Terminal/Levels")):
                if (os.path.exists(f"{values().get_base_directory()}/Terminal/logs")):
                    if (os.path.exists(f"{values().get_base_directory()}/Terminal/Resources")):
                        if (os.path.exists(f"{values().get_base_directory()}/Terminal/Resources/langs")):
                            return True
                    else:
                        os.makedirs(f"{values().get_base_directory()}/Terminal/Resources/langs")
                else:
                    os.makedirs(f"{values().get_base_directory()}/Terminal/logs")
            else:
                os.makedirs(f"{values().get_base_directory()}/Terminal/Levels")
        else:
            os.makedirs(f"{values().get_base_directory()}/Terminal")

    def get_level(self) -> Level:

        def when_list(obj: list) -> list:
            lst = []
            for i, value in enumerate(obj):
                if (isinstance(value, str)):
                    lst.append(str(base.get(keyb)))
                elif (isinstance(value, list)):
                    lst.append(when_list(list(value)))
                elif (isinstance(value, bool) or isinstance(value, int)):
                    lst.append(value)
                else:
                    Logger().log(
                        f"Cant import unknown data state from activate.json in target of level. Data: <{value}>")
            return lst

        with open("backend/preFiles/app/activate.json", "r") as read_file:
            data = json.load(read_file)
        data = dict(data)
        level = Level([])
        for build_key in data.keys():
            if (build_key == "target"):
                for keya in dict(data.get(build_key)).keys():
                    base = dict(dict(data.get(build_key)).get(keya))
                    command = []
                    for index, keyb in enumerate(base.keys()):
                        if (keyb != "type"):
                            if (isinstance(base.get(keyb), str)):
                                command.append(f"\"{str(base.get(keyb))}\"")
                            elif (isinstance(base.get(keyb), list)):
                                command.append(f"[{when_list(list(base.get(keyb)))}]")
                            elif (isinstance(base.get(keyb), bool) or isinstance(base.get(keyb), int)):
                                command.append(f"{base.get(keyb)}")
                            else:
                                Logger().log(f"Cant import unknown data state from activate.json in target of level. Data: <{base.get(keyb)}>")
                        else:
                            continue
                    class_obj = globals()[keya]
                    FE = "class_obj("
                    for i, val in enumerate(command):
                        FE = FE + val
                        if (len(command) != (i+1)):
                            FE = FE + ", "
                    FE = FE + ")"
                    obj = _based(exec(FE))
                    level.req = obj
            build = dict(data.get(build_key))
            building = Building([])
            for fl_key in build.keys():
                fl = dict(build.get(fl_key))
                floor = Floor([])
                for room in fl.values():
                    floor.append(Room(items=dict(room).get("items"), name=dict(room).get("name"), blocked=dict(room).get("blocked")))
                building.append(floor)
            level.append(building)
        return level

    def save_level(self) -> None:
        name = stack().get_stack().get(values().get_base_level_name_stack_cont())
        path = f"{values().get_base_directory()}/Terminal/Levels/{stack().get_stack().get(values().get_base_level_name_stack_cont())}.json"
        if (name != None and os.path.exists(f"{values().get_base_directory()}/Terminal/Levels/{name}.json")):
            try:
                del name
                open(path, "w+").close()
                with open("backend/preFiles/app/activate.json", "r") as read_file:
                    data = json.load(read_file)
                data = dict(data)
                with open(path, "w") as write_file:
                    json.dump(data, write_file)
                Logger().log(f"Success save active level from activate.json to his file. Save to: <{path}>.")
            except:
                self.Game(self.get_level()).cmd(frontend.Menu.root.MENUs).update_terminal_text(
                    language().__getitem__("save_level_error_message"), username="FATAL ERROR")
                Logger().log(f"In process of save active level was appeared error!")
        else:
            Logger().log(f"Can't save level to <{path}>.")

    def ImageCheck(self) -> bool:
        if (os.path.exists(values().get_base_resources_directory())):
            if (os.path.exists(values().get_base_menu_button_image_directory())):
                return True
            else:
                Logger().log("Attempt to save image..")
                req = None
                for i in range(4):
                    try:
                        req = requests.get(values().get_url_menu_button_image())
                        if (req.status_code == 200):
                            with open(values().get_base_menu_button_image_directory(), 'wb') as f:
                                f.write(req.content)
                            Logger().log("Success attempt save!")
                            del req
                            return True
                    except:
                        Logger().log(f"Lose attempt {i + 1}. Status code: {req.status_code}")
        else:
            os.mkdir(values().get_base_resources_directory())
            Logger().log("Resources directory was been created.")
            Logger().log("Attempt to save image..")
            req = None
            for i in range(4):
                try:
                    req = requests.get(values().get_url_menu_button_image())
                    if (req.status_code == 200):
                        with open(values().get_base_menu_button_image_directory(), 'wb') as f:
                            f.write(req.content)
                        Logger().log("Success attempt save!")
                        del req
                        return True
                except:
                    Logger().log(f"Lose attempt {i+1}. Status code: {req.status_code}")
        return False



