from backend.commands.basedCommand import based
import backend

class clear(based):
    """
    This func needs to scroll terminal window down after command <c>
    """

    def cast(self, line: backend.commands.commandLine) -> list[str]:
        super().cast(line)
        return ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]