import threading
import time
from atexit import register
import keyboard

from backend.funcs.generate_play_space import Generate
from based.gate import Gate
from based.Logger import Logger
from based.based_values import values
from frontend.Menu.root import mTk
from frontend.Game.window import Tk
from frontend.Menu.root import MENUs
from frontend.Game.window import ROOTs

import frontend

class __started():

    def __init__(self):
        pass

    def on_enter(self) -> None:
        """Activate loop listener \"Enter\" key on keyboard"""

        Logger().log("Keyboard listener has being started.")
        while True:
            if (keyboard.is_pressed("enter")):
                Gate().Game(Gate().get_level()).cmd(ROOTs).activate_command()
                Gate().save_level()
                time.sleep(1)
            else:
                time.sleep(0.1)
                continue

    def __on_enter_menu(self) -> None:
        Logger().log("Menu keyboard listener has being started.")
        while True:
            if (keyboard.is_pressed("enter")):
                Gate().Game(Gate().get_level()).VE(MENUs).activate_command()
                Gate().save_level()
                time.sleep(1)
            else:
                time.sleep(0.1)
                continue

    def __import(self):
        """Main func for import and load all files and start all systems"""

        Logger().log("Import threading has being started.")
        Generate().generate()
        frontend.Game.window.ROOTs = Tk(
            background=values().get_base_bg_color(),
            title=values().get_base_title(),
            sizes=values().get_base_sizes()
        )

    def start(self):
        """Main func"""

        frontend.Menu.root.MENUs = mTk(
            background=values().get_base_menu_bg(),
            title=values().get_base_menu_title(),
            sizes=values().get_base_sizes()
        )
        Logger().log("New menu window has being created.")
        self.__import()
        th = threading.Thread(target=self.__on_enter_menu, daemon=True)
        th.start()
        MENUs.get_root().mainloop()

thread = threading.Thread(target=__started().on_enter, daemon=True)
counter = threading.Thread(target=Gate().counter, daemon=True)
register(Gate().clear, "602")

__started().start()
#thread.start()
#counter.start()
#ROOT.get_root().mainloop()




