import backend.funcs.generate_play_space

class line():

    def __init__(self, command: list[str], level: backend.funcs.generate_play_space.Level):
        self.command = command
        self.Level = level