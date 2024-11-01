from json import load
import based
from based.based_values import values

class _JSON():

    def __init__(self, path: str):
        self.path = path

    def _get_json_file(self) -> dict:
        with open(self.path, "r", encoding="UTF-8") as line:
            data = load(line)
        return data

class color():

    def __init__(self, color: str = ""):
        self.color = color
        self.Logger = based.gate.Logger()
        self.__check()

    def __get_colors_path(self) -> str:
        return "backend/preFiles/app/colors.json"

    def __check(self):
        if (len(self.__get_colors_path()) <= 5):
            self.Logger.log(f"JSON file with colors is not exist! File path (That returned by a func) <{self.__get_colors_path()}>. Setting color value to base.")
            self.color = values().get_based_text_color()
        colors = _JSON(self.__get_colors_path())._get_json_file()
        if (len(colors) == 0):
            self.Logger.log(
                f"JSON file with colors is empty or not defined! JSON File <{self.__get_colors_path()}>. Setting color value to base.")
            self.color = values().get_based_text_color()
        for key in colors.keys():
            if (str(self.color).lower() == str(key).lower()):
                return True
            else:
                continue
        self.Logger.log(f"Not found registered color with name <{self.color}>. Setting color value to base.")
        self.color = values().get_based_text_color()

