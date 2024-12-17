import json
import os.path

from based.Logger import Logger, stack
from based.based_values import values

class _langs():

    def __get(self, d: dict) -> str:
        for key in d.keys():
            return str(key)

    def __getstate__(self) -> dict[str: list[str]]:
        path = f"{values().get_base_resources_directory()}/langs"
        if (os.path.exists(path)):
            lst = os.listdir(path)
            if (len(lst) == 0):
                Logger().log(f"Was appeared a error because language directory is empty!")
                raise LanguageException
            else:
                languages = {}
                for dir in lst:
                    if (not os.path.isfile(str(path + "/" + dir))):
                        pat = f"{path}/{dir}"
                        if len(os.listdir(pat)) == 0:
                            Logger().log(f"Can't import language package because needs files are not be found! Path: {pat}")
                        else:
                            for file in os.listdir(pat):
                                if (str(file) == "getter.json"):
                                    with open(f"{pat}/getter.json", "r", encoding="utf-8") as read_file:
                                        data = json.load(read_file)
                                    data = dict(data)
                                    languages[str(self.__get(data))] = list(data.get(str(self.__get(data))))
                                    break
                                else:
                                    continue
                    else:
                        continue
                if (len(languages.keys()) == 0):
                    Logger().log("No one language not be imported!")
                    raise LanguageException
                else:
                    return languages
        else:
            Logger().log("No one language not be imported!")
            raise LanguageException

class LanguageException(BaseException):

    def __init__(self, *args):
        super().__init__(*args)

class ItemLanguageException(BaseException):

    def __init__(self, *args):
        super().__init__(*args)

class language:
    global _langs

    def __init__(self):
        self.lan = ""
        self.base_path = ""

    def __check(self) -> str:
        """
        :return: Base path with all files of this language in Resources directory
        """
        for key in dict(_langs().__getstate__()).keys():
            value = list(dict(_langs().__getstate__()).get(key))
            if (self.lan in value):
                self.lan = value[0]
                del value
                self.base_path = f"{values().get_base_resources_directory()}/langs/{key}"
                return f"{values().get_base_resources_directory()}/langs/{key}"
        return None

    def set_lang(self, lan: str):
        self.lan = lan
        self.__check()
        if len(self.base_path) == 0:
            Logger().log(f"System cant set \"{lan}\" language because he is not be found.")
            raise LanguageException
        path = values().get_base_resources_directory()
        if (os.path.exists(path)):
            open((path + "/language.txt"), "w+").close()
            f = open((path + "/language.txt"), "w+")
            f.write(self.lan)
            f.close()
            stack().controller({"lang": self.lan})
            Logger().log(f"System changed to \"{self.lan}\" language!")
            del path
        else:
            os.mkdir(path)
            self.set_lang(lan=lan)

    def get_lang(self) -> str:
        """
        :return: the first element of list who language set now
        """
        path = values().get_base_resources_directory()
        if (os.path.exists(path + "/language.txt")):
            f = open((path + "/language.txt"), "r")
            file = list(f.readlines())[0].replace("\n", "")
            f.close()
            return file
        else:
            os.mkdir(path)
            self.set_lang("EN")
            return "enEN"

    def __getitem__(self, item: str, args: dict = None) -> list[str]:
        self.lan = self.get_lang()
        base_path = f"{values().get_base_resources_directory()}/langs/{self.lan}"
        with open(f"{base_path}/common.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        common_data = dict(data)
        if (item in common_data.keys()):
            del base_path
            res = list(common_data.get(item))
            if (args is not None):
                for i in range(len(res)):
                    for key in args.keys():
                        res[i] = res[i].replace(key, args.get(key))
            return res
        with open(f"{base_path}/driver.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        driver_data = dict(data)
        if (item in driver_data.keys()):
            path = base_path + "/" + driver_data.get(item)
            del base_path
            f = open(path, "r", encoding="utf-8")
            message = f.readlines()
            f.close()
            for i in range(len(message)):
                if "\n" in message[i]:
                    message[i] = message[i].replace("\n", "")
            del path
            return message
        raise ItemLanguageException



