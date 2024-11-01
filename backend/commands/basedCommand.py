from backend.commands.commandLine import line

class based(line):
    """
    This base-class for anything command.
    In this class will be created util funcs and other fun things.
    """

    def __init__(self):
        super().__init__([], [])
        pass

    def cast(self, cl: line) -> list[str]:
        """
        This classic func for anything command.
        This func keeps all logic of command.
        """
        pass