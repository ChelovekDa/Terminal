from json import load
from based.gate import Logger
from random import choice

class _JSON():

    def __init__(self, path: str):
        self.path = path

    def _get_json_file(self) -> dict:
        with open(self.path, "r", encoding="UTF-8") as line:
            data = load(line)
        return data

class color():

    class based_colors():

        def get_base_bg(self) -> str:
            return "black"

        def get_base_button_color(self) -> str:
            return "white"

        def get_based_text_color(self) -> str:
            return "limegreen"

    def __init__(self, color: str = ""):
        self.color = color
        self.__check()

    def __get_colors_path(self) -> str:
        return "backend/preFiles/app/colors.json"

    def __check(self):
        if (len(self.__get_colors_path()) <= 5):
            Logger().log(f"JSON file with colors is not exist! File path (That returned by a func) <{self.__get_colors_path()}>. Setting color value to base.")
            self.color = self.based_colors().get_based_text_color()
        colors = _JSON(self.__get_colors_path())._get_json_file()
        if (len(colors) == 0):
            Logger().log(
                f"JSON file with colors is empty or not defined! JSON File <{self.__get_colors_path()}>. Setting color value to base.")
            self.color = self.based_colors().get_based_text_color()
        for key in colors.keys():
            if (str(self.color).lower() == str(key).lower()):
                return True
            else:
                continue
        Logger().log(f"Not found registered color with name <{self.color}>. Setting color value to base.")
        self.color = self.based_colors().get_based_text_color()

