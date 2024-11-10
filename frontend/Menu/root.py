import tkinter

from frontend.Game.window import Tk

class mTk(Tk):

    def __init__(self, background: str = "", title: str = "", sizes: list[int] = None):
        super().__init__(background=background, title=title, sizes=sizes)

    def get_root(self) -> tkinter.Tk:
        global MENU
        MENU = super().get_root()
        return MENU

MENUs = mTk()