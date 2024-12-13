import tkinter

from backend.commands.basedCommand import based
from backend.commands.commandLine import line
from frontend.Menu.root import MENUs

class delete(based):

    def __init__(self):
        super().__init__()

    def other_cast(self) -> list[str]:
        MENUs.listbox.delete(0, tkinter.END)
        MENUs.listbox.insert(0, "")
        return []

    def cast(self, cl: line) -> list[str]:
        return self.other_cast()