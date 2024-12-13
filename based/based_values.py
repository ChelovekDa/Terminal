from random import randint
import os
from getpass import getuser

class values:

    class file_names:

        def get_change_command_help_message_file_name(self) -> str:
            return "change_help_command"

    def get_base_game_time_stack(self) -> str:
        return "GameTime"

    def get_base_level_name_stack_cont(self) -> str:
        return "LevelName"

    def get_base_bg(self) -> str:
        return "gray17"

    def get_base_terminal_bg(self) -> str:
        return "gray18"

    def get_base_terminal_system_username(self) -> str:
        return ""

    def get_base_menu_bg(self) -> str:
        return self.get_base_bg()

    def get_stack_spliter(self) -> str:
        return "/*/="

    def get_base_title(self) -> str:
        return "T E R M I N A L"

    def get_base_sizes(self) -> list[int]:
        return [1200, 700]

    def get_base_background_color(self) -> str:
        return self.get_base_bg()

    def get_base_list_round_console_lines(self) -> list[float]:
        return [0.7, 0.8, 0.9, 1.0]

    def get_base_menu_title(self) -> str:
        return self.get_base_title()

    def get_base_stack_for_last_level_created_name(self) -> str:
        return "lastLevelName"

    def get_base_directory(self) -> str:
        return f"{os.environ['SYSTEMDRIVE']}/Users/{getuser()}/AppData/Roaming/HCC"

    def get_base_resources_directory(self) -> str:
        return f"{self.get_base_directory()}/Terminal/Resources"

    def get_base_terminal_message(self) -> list[str]:
        f = open("backend/preFiles/app/terminal_base_message", "r")
        message = []
        for line in f.readlines():
            line = line.replace("\n", "")
            if ("{number}" in line):
                line = line.replace("{number}", str(randint(1111111111, 9999999999)))
            elif ("{name}" in line):
                line = line.replace("{name}", "$USER5$-G")
            line = "  " + line
            message.append(line)
        return message

    def get_base_button_color(self) -> str:
        return "mediumseagreen"

    def get_based_text_color(self) -> str:
        return "limegreen"

    def get_base_menu_button_image_directory(self) -> str:
        return f"{self.get_base_resources_directory()}/back_image.png"

    def get_base_username(self) -> str:
        return "$USER5$-G"

    def get_url_menu_button_image(self) -> str:
        return "https://www.pngarts.com/files/8/Round-Back-Button-PNG-Image-Background.png"