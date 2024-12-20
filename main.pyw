import threading
import time
import tkinter
from atexit import register
import keyboard
import sys
from libs import pyperclip

from backend.funcs.generate_play_space import Generate
from based.gate import Gate
from based.Logger import Logger, stack
from based.based_values import values
from based.langist import language
from frontend.Menu.root import mTk
from frontend.Menu.root import MENUs

import frontend

last_command = ""

class __started():

    def __copy_loop(self) -> None:
        global last_command
        while True:
            if (keyboard.is_pressed("shift+insert")):
                pyperclip.copy(last_command)
            else:
                time.sleep(0.01)

    def on_enter(self) -> None:

        def toN_check(arg) -> bool:
            if (arg == "True"):
                return True
            return False

        global last_command
        first_command = True
        Logger().log("Keyboard listener has being started.")
        while True:
            if (keyboard.is_pressed("enter")):
                toN = stack().get_stack().get("from_terminal")
                if (first_command):
                    Gate().Game(Gate().get_level()).cmd(MENUs).update_terminal_text([], "|", True)
                    first_command = False
                try:
                    if (toN_check(toN)):
                        last_command = Gate().Game(Gate().get_level()).cmd(MENUs).activate_command()
                    else:
                        last_command = Gate().Game(Gate().get_level()).VE(MENUs).activate_command()
                except RecursionError as e:
                    Logger().log(
                        f"In process of execute command was appeared a error. Error: <{e}>")
                    Gate().Game(Gate().get_level()).cmd(MENUs).update_terminal_text(language().__getitem__("on_enter_RecursionError"),"|")
                Gate().save_level()
                MENUs.entry.yview_moveto(float("inf"))
                MENUs.entry.delete("1.0", tkinter.END)
                time.sleep(1)
            else:
                time.sleep(0.01)
                continue

    def start(self):
        """Main func"""
        sys.setrecursionlimit(3000)
        Gate().check()
        Logger().log("Setting recursion limit to 3000.")
        Generate().generate()
        frontend.Menu.root.MENUs = mTk(
            background=values().get_base_menu_bg(),
            title=values().get_base_menu_title(),
            sizes=values().get_base_sizes()
        )
        stack().controller({"from_terminal": "False"})
        Logger().log("New menu window has being created.")

thread = threading.Thread(target=__started().on_enter, daemon=True)
counter = threading.Thread(target=Gate().counter, daemon=True)
register(Gate().clear, "602")

__started().start()
thread.start()
counter.start()
print(stack().get_stack())
MENUs.get_root().mainloop()




