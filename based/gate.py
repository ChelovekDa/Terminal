import io
import os
from getpass import getuser
import datetime

class Gate():
    """
    This main class for all FUNCs.
    Gate - class with all methods for app.
    main.py - main class of all APP.

    Classes:
    * stack() - class for manage and use the stack file.
    * visible() - class for get and manage the frontend part of app.
    * hub() - class for work and manage commands of app.
    """

    class stack():
        """
        This class needs to use and manage the stack.
        """

        def __get_stack_spliter(self) -> str:
            return "/*/="

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
            try:
                stak = self.get_stack()
                open(self.__get_based_stack_path(), "w").close()
                stack = open(self.__get_based_stack_path(), "w", encoding="UTF-8")
                for key in stak.keys():
                    stack.write((f"{key}{self.__get_stack_spliter()}{stak.get(key)}\n"))
                if (type(data) == list):
                    data = list(data)
                    for item in data:
                        if (type(item) == list):
                            stack.write((f"{item[0]}{self.__get_stack_spliter()}{item[1]}"))
                        else:
                            if (len(data) == 2):
                                stack.write((f"{data[0]}{self.__get_stack_spliter()}{data[1]}"))
                                break
                elif (type(data) == str):
                    data = str(data)
                    if (data.find(self.__get_stack_spliter()) == -1):
                        stack.write((f" {self.__get_stack_spliter()}{data}"))
                    else:
                        stack.write((data))
                elif (type(data) == dict):
                    data = dict(data)
                    for key in data.keys():
                        stack.write((f"{key}{self.__get_stack_spliter()}{data.get(key)}"))
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
                sp = line.split(self.__get_stack_spliter())
                if (len(sp) == 2):
                    res[sp[0]] = sp[1]
            return res

        def clear(self, password) -> None:
            if (str(password) == self.__get_stack_cleared_password()):
                Logger().log(f"Stack is being cleared!")
                open("based/stack.txt", "w+").close()
            else:
                Logger().log(f"Stack has not been cleared because password is not correctly. {password}/{self.__get_stack_cleared_password()}")
                return None

    def get_base_directory(self) -> str:
        return f"{os.environ['SYSTEMDRIVE']}/Users/{getuser()}/AppData/Roaming/HCC"

    class hub():

        def register(self, command) -> None:
            Logger().log(f"Register new command action. Command line: {command}")


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



