import atexit

from backend.funcs.generate_play_space import Generate
from frontend.window import Tk, based_values
from based.gate import Gate

atexit.register(Gate().stack().clear, "602")

LEVEL = None
ROOT = Tk()

class __started():

    def __init__(self):
        pass

    def _import_(self):
        """Main func for import and load all files and start all systems"""
        global LEVEL, ROOT
        LEVEL = Generate().generate()
        ROOT = Tk(
            background=based_values().get_base_bg_color(),
            title=based_values().get_base_title(),
            sizes=based_values().get_base_sizes()
        )

    def _get_intro(self):
        """After start all systems and load of all needed files, user watches the game's intro."""
        pass

__started()._import_()
#ROOT.get_root().mainloop()




