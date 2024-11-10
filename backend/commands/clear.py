from backend.commands.basedCommand import based
import backend

class clear(based):
    """
    This func needs to scroll terminal window down after command <c>
    """

    def __init__(self, from_t: bool = False):
        self.from_t = from_t
        super().__init__()

    def cast(self, line: backend.commands.commandLine) -> list[str]:
        super().cast(line)
        return ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]