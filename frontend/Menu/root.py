import tkinter

from frontend.Game.window import Tk

class mTk(Tk):

    def __init__(self, background: str = "", title: str = "", sizes: list[int] = []):
        super().__init__(background=background, title=title, sizes=sizes)

    def get_root(self) -> tkinter.Tk:
        global MENUs
        MENUs = super().get_root()
        return MENUs

MENUs = mTk()