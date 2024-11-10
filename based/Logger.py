import os
import datetime
import io

from based.based_values import values

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
                Logger().log(
                    f"Cannot open or write the data in stack, and \"Gate\" can't open the stack file. \ndata: {data}")

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
            Logger().log(
                f"Stack has not been cleared because password is not correctly. {password}/{self.__get_stack_cleared_password()}")
            return False

class Logger():

    def __new_log_name(self) -> str:
        return f"{values().get_base_directory()}/Terminal/logs/{str(datetime.datetime.now().year)}-{str(datetime.datetime.now().month)}-{str(datetime.datetime.now().day)}-{str(datetime.datetime.now().hour)}-{str(datetime.datetime.now().minute)}-{str(datetime.datetime.now().second)}"

    def __read_log(self) -> list[str]:
        file_name = stack().get_stack().get("log_name")
        if (file_name != "None" or None):
            try:
                return open(file_name, "r", encoding="UTF-8").readlines()
            except:
                return []
        else:
            return []

    def log(self, message: str):
        self.createLogDir()
        stackn = stack().get_stack()
        if (stackn.get("log_name") != "None" or None):
            latest = self.__read_log()
            file = None
            try:
                file = open(stack().get_stack().get("log_name"), "w+", encoding="UTF-8")
                for line in latest:
                    file.write((line))
                file.write((f"[{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}] {message}\n"))
            except:
                name = self.__new_log_name()
                file = open(name, "w+", encoding="UTF-8")
                file.write((f"[{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}] {message}\n"))
                try:
                    stack().controller({"log_name": name})
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
            stack().controller({"log_name": name})
            file = open(name, "w+", encoding="UTF-8")
            file.write((f"[{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}] {message}\n"))
            file.close()

    def createLogDir(self) -> bool:
        if (os.path.exists(f"{values().get_base_directory()}/Terminal/logs")):
            return True
        else:
            os.mkdir(values().get_base_directory())
            os.mkdir(f"{values().get_base_directory()}/Terminal")
            os.mkdir(f"{values().get_base_directory()}/Terminal/logs")
            return True