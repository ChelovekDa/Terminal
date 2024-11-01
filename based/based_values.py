from random import randint

class values():

    def get_base_bg(self) -> str:
        return "cyan"

    def get_stack_spliter(self) -> str:
        return "/*/="

    def get_base_title(self) -> str:
        return "T E R M I N A L"

    def get_base_sizes(self) -> list[int]:
        return [1200, 700]

    def get_base_bg_color(self) -> str:
        return self.get_base_bg()

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
        return "white"

    def get_based_text_color(self) -> str:
        return "limegreen"

    def get_base_username(self) -> str:
        return "$USER5$-G"