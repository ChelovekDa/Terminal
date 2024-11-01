import threading
import time
from atexit import register
import keyboard

from backend.funcs.generate_play_space import Generate, Level
from frontend.Game.window import Tk
from based.gate import Gate, Logger
from based.based_values import values

LEVEL = Level
ROOT = Tk()
LOGGER = Logger
GATE = Gate

def on_enter() -> None:
    global LEVEL, ROOT
    while True:
        if (keyboard.is_pressed("enter")):
            LEVEL = Gate().Game(LEVEL).cmd(ROOT).activate_command()
            time.sleep(1)
        else:
            time.sleep(0.1)
            continue

thread = threading.Thread(target=on_enter, daemon=True)

register(Gate().clear, "602")

class __started():

    def __init__(self):
        pass

    def _import_(self):
        """Main func for import and load all files and start all systems"""
        global LEVEL, ROOT, LOGGER, GATE
        GATE = Gate()
        LOGGER = Logger()
        LEVEL = Generate().generate()
        ROOT = Tk(
            background=values().get_base_bg_color(),
            title=values().get_base_title(),
            sizes=values().get_base_sizes()
        )

    def _get_intro(self):
        """After start all systems and load of all needed files, user watches the game's intro."""
        pass

__started()._import_()
thread.start()
ROOT.get_root().mainloop()




