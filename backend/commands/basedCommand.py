from backend.commands.commandLine import line

class based(line):
    """
    This base-class for anything command.
    In this class will be created util funcs and other fun things.
    """

    def __init__(self, padding: int = 0, cl: line = line([], [])):
        self.padding = padding
        self.cl = cl
        super().__init__(cl.command, cl.Level)

    def get(self, index: int) -> str:
        l = self.cl.command
        ind = index
        pad = self.padding
        return self.cl.command[index + self.padding]

    def __len__(self) -> int:
        return len(self.cl.command) - self.padding

    def help(self) -> list[str]:
        pass

    def check(self, cl: line):
        if (cl.command[0] in ["VE", "ve"]):
            self.padding = 1
        else:
            self.padding = 0

    def cast(self, cl: line) -> list[str]:
        """
        This classic func for anything command.
        This func keeps all logic of command.
        """
        pass