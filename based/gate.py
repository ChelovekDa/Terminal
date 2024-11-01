import io
import tkinter
from getpass import getuser
import os
import datetime

from backend.commands.basedCommand import based
from backend.commands.ping import ping
from backend.commands.use import use
from backend.commands.clear import clear
from backend.commands.list import list as lst
from backend.commands.commandLine import line

from frontend.Game.window import Tk
from backend.funcs.generate_play_space import Level as Level
from based.based_values import values

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
        """

        LEVEL = Level

        def __init__(self, level: Level):
            global LEVEL
            LEVEL = level

        class cmd():

            def __init__(self, terminal_root: Tk):
                self.root = terminal_root

            def update_terminal_text(self, new_text: list[str], username: str = values().get_base_username(), replace: bool = False) -> Tk:
                """
                This function needs to update text on user Terminal when him playing and adding new information.

                :argument new_text - text that you want to print to user screen.
                :argument replace - are you want to delete all information on terminal screen and replace it?
                """
                if (replace):
                    self.root.listbox.delete(0, tkinter.END)
                    self.root.listbox.insert(0, "")
                    for i in range(len(new_text)):
                        self.root.listbox.insert(i+1, f"  <{username}>: {new_text[i]}")
                    return self.root
                else:
                    index = self.root.listbox.size()
                    for line in new_text:
                        self.root.listbox.insert(index, f"  <{username}>: {line}")
                        index+=1
                    return self.root

            def __get_command_catalogue(self) -> dict[str, based]:
                catalogue = {
                    "ping": ping(),
                    "use": use(),
                    "c": clear(),
                    "list": lst()
                }
                return catalogue

            def __convert(self, command_arg: str) -> list[str]:
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

            def activate_command(self):
                """
                This function need to do the commands from terminal that user entered.
                command - this parameter contains a list with all command lines that user entered.
                """

                command = self.__convert(str(self.root.entry.get("1.0", tkinter.END)))

                if (self.__get_command_catalogue().get(command[0]) == None):
                    self.update_terminal_text(["This command wasn't be applied! This command is not to be found.", ""])
                    Logger().log(f"Command <{str(command)}> is not be found.")
                else:
                    if (len(command) >= 2 and command[1] != ""):
                        self.update_terminal_text(self.__get_command_catalogue().get(command[0]).cast(line(command, LEVEL)))
                        Logger().log(f"Was been applied command <{str(command)}>")
                    else:
                        Logger().log(f"Command <{str(command)}> cant be applied.")
                        self.update_terminal_text(["This command cant be applied because text length less than need."])

    class stack():
        """
        This class needs to use and manage the stack.
        """

        def __get_stack_cleared_password(self) -> str:
            """Return the password, that need to clear the stack file.
            This private func for other classes and funcs inside app."""
            return "602"

        def __get_based_stack_path(self) -> str:
            return "based/stack.txt"

        def controller(self, data):
            """
            This func needs to manage the stack file and write new lines in his.
            This private func for other classes and funcs inside app.
            """
            stack = None
            spliter = values().get_stack_spliter()
            try:
                stak = self.get_stack()
                open(self.__get_based_stack_path(), "w").close()
                stack = open(self.__get_based_stack_path(), "w", encoding="UTF-8")
                for key in stak.keys():
                    stack.write((f"{key}{spliter}{stak.get(key)}\n"))
                if (type(data) == list):
                    data = list(data)
                    for item in data:
                        if (type(item) == list):
                            stack.write((f"{item[0]}{spliter}{item[1]}"))
                        else:
                            if (len(data) == 2):
                                stack.write((f"{data[0]}{spliter}{data[1]}"))
                                break
                elif (type(data) == str):
                    data = str(data)
                    if (data.find(values().get_stack_spliter()) == -1):
                        stack.write((f" {spliter}{data}"))
                    else:
                        stack.write((data))
                elif (type(data) == dict):
                    data = dict(data)
                    for key in data.keys():
                        stack.write((f"{key}{spliter}{data.get(key)}"))
                stack.close()
                return None
            except:
                try:
                    Logger().log(f"Cannot open or write the data in stack. Stack: {self.get_stack()}.\ndata: {data}")
                    stack.close()
                except:
                    Logger().log(f"Cannot open or write the data in stack, and \"Gate\" can't open the stack file. \ndata: {data}")

        def get_stack(self) -> dict:
            res = {}
            f = open(self.__get_based_stack_path(), "r", encoding="UTF-8")
            file = f.readlines()
            f.close()
            for line in file:
                if "\n" in line:
                    line = line.replace("\n", "")
                sp = line.split(values().get_stack_spliter())
                if (len(sp) == 2):
                    res[sp[0]] = sp[1]
            return res

        def clear(self, password) -> bool:
            if (str(password) == self.__get_stack_cleared_password()):
                Logger().log(f"Stack is being cleared!")
                open("based/stack.txt", "w+").close()
                return True
            else:
                Logger().log(f"Stack has not been cleared because password is not correctly. {password}/{self.__get_stack_cleared_password()}")
                return False

    def get_base_directory(self) -> str:
        return f"{os.environ['SYSTEMDRIVE']}/Users/{getuser()}/AppData/Roaming/HCC"

    def clear(self, password: str) -> None:
        """This function need to clear all program files."""
        if (self.stack().clear(password)):
            open("backend/prefiles/app/activate.json", "w+").close()
        return None

class Logger():

    def __new_log_name(self) -> str:
        return f"{Gate().get_base_directory()}/Terminal/logs/{str(datetime.datetime.now().year)}-{str(datetime.datetime.now().month)}-{str(datetime.datetime.now().day)}-{str(datetime.datetime.now().hour)}-{str(datetime.datetime.now().minute)}-{str(datetime.datetime.now().second)}"

    def __read_log(self) -> list[str]:
        file_name = Gate().stack().get_stack().get("log_name")
        if (file_name != "None" or None):
            try:
                return open(file_name, "r", encoding="UTF-8").readlines()
            except:
                return []
        else:
            return []

    def log(self, message: str):
        self.createLogDir()
        stack = Gate().stack().get_stack()
        if (stack.get("log_name") != "None" or None):
            latest = self.__read_log()
            file = None
            try:
                file = open(Gate().stack().get_stack().get("log_name"), "w+", encoding="UTF-8")
                for line in latest:
                    file.write((line))
                file.write((f"[{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}] {message}\n"))
            except:
                name = self.__new_log_name()
                file = open(name, "w+", encoding="UTF-8")
                file.write((f"[{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}] {message}\n"))
                try:
                    Gate().stack().controller({"log_name": name})
                except:
                    if (isinstance(file, io.TextIOWrapper)):
                        file.close()
                        return None
                    else:
                        return None
            finally:
                if (isinstance(file, io.TextIOWrapper)):
                    file.close()
                else:
                    return None
        else:
            name = self.__new_log_name()
            Gate().stack().controller({"log_name": name})
            file = open(name, "w+", encoding="UTF-8")
            file.write((f"[{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}] {message}\n"))
            file.close()

    def createLogDir(self) -> bool:
        if (os.path.exists(f"{Gate().get_base_directory()}/Terminal/logs")):
            return True
        else:
            os.mkdir(Gate().get_base_directory())
            os.mkdir(f"{Gate().get_base_directory()}/Terminal")
            os.mkdir(f"{Gate().get_base_directory()}/Terminal/logs")
            return True



