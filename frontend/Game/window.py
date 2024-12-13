import tkinter
from tkinter import ttk

from based.Logger import Logger
from based.based_values import values

class Tk():
    ROOT = tkinter.Tk

    def __init__(self, background: str = "", terminal_bg: str = values().get_base_terminal_bg(), title: str = "", sizes: list[int] = []):
        if (background == ""):
            background = values().get_base_background_color()
        self.background = background
        self.title = title
        if (len(sizes) == 2):
            for i in range(len(sizes)):
                sizes[i] = self.__to_int(str(sizes[i]))
        else:
            sizes = values().get_base_sizes()
        self.sizes = sizes
        self.listbox = tkinter.Listbox
        self.entry = tkinter.Text
        self.tbg = terminal_bg

    def __strippers(self, arg: list[str]) -> tkinter.StringVar:
        for i in range(14):
            arg.append("")
        return tkinter.StringVar(value=arg)

    def __to_int(self, str: str) -> int:
        try:
            return int(str)
        except:
            Logger().log(f"The size of window is not int. The window will be made to square form. Arg: \"{str}\"")
            return 600

    def on_scroll(self, *args):
        if self.entry.yview()[1] >= 1.0:
            self.entry.yview_moveto(float("inf"))

    #chartreuse3
    #mediumseagreen
    def get_root(self) -> tkinter.Tk:
        global ROOT
        root = tkinter.Tk()
        root["bg"] = self.background
        root.title(self.title)
        root.geometry('%dx%d+%d+%d' % (self.sizes[0], self.sizes[1], (root.winfo_screenwidth() / 2) - (self.sizes[0] / 2), (root.winfo_screenheight() / 2) - (self.sizes[1] / 2)))
        root.resizable(width=False, height=False)

        self.listbox = tkinter.Listbox(listvariable=self.__strippers(values().get_base_terminal_message()), background=self.background, font=("Better VCR", 12), foreground="springgreen3", activestyle="none")
        self.listbox.bind("<<ListboxSelect>>", lambda x: self.listbox.selection_clear(0, tkinter.END))
        self.listbox.pack(side="left", fill="both", expand=1)
        scrollbar = ttk.Scrollbar(orient="vertical", command=self.on_scroll, takefocus=False)
        scrollbar.pack(side="right", fill="y")
        self.listbox["yscrollcommand"] = scrollbar.set

        self.entry = tkinter.Text(relief="sunken", background=self.tbg, foreground="springgreen3", font=("Better VCR", 12), width=98, height=12, wrap=tkinter.WORD)
        self.entry.place(x=1, y=502)

        ROOT = root
        return root

ROOTs = Tk()


