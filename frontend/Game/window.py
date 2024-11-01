import tkinter
from tkinter import ttk

import based
import based.Color
from based.based_values import values

class Tk():
    ROOT = tkinter.Tk

    def __init__(self, background: str = "", title: str = "", sizes: list[int] = []):
        self.background = background
        self.title = title
        for i in range(len(sizes)):
            sizes[i] = self.__to_int(str(sizes[i]))
        self.sizes = sizes
        self.listbox = tkinter.Listbox
        self.entry = tkinter.Text
        self.Logger = based.gate.Logger()

    def __strippers(self, arg: list[str]) -> tkinter.StringVar:
        for i in range(14):
            arg.append("")
        return tkinter.StringVar(value=arg)

    def __to_int(self, str: str) -> int:
        try:
            return int(str)
        except:
            self.Logger.log(f"The size of window is not int. The window will be made to square form. Arg: \"{str}\"")
            return 600

    def get_root(self) -> tkinter.Tk:
        global ROOT

        root = tkinter.Tk()
        root["bg"] = self.background
        root.title(self.title)
        root.geometry('%dx%d+%d+%d' % (self.sizes[0], self.sizes[1], (root.winfo_screenwidth() / 2) - (self.sizes[0] / 2), (root.winfo_screenheight() / 2) - (self.sizes[1] / 2)))
        root.resizable(width=False, height=False)

        data = ['Once upon a midnight dreary,\n', 'While I pondered, weak and weary,\n', 'Over many a quaint and curious\n', 'Volume of forgotten lore—\n', 'While I nodded, nearly napping,\n', 'Suddenly there came a tapping,\n', 'As of some one gently rapping,\n', 'Rapping at my chamber door.\n', '"\'T is some visitor," I muttered,\n', '"Tapping at my chamber door\n', 'Only this and nothing more."\n', 'Ah, distinctly I remember,\n', 'It was in the bleak December,\n', 'And each separate dying ember\n', 'Wrought its ghost upon the floor.\n', 'Eagerly I wished the morrow;\n', 'Vainly I had sought to borrow\n', 'From my books surcease of sorrow\n', 'Sorrow for the lost Lenore—\n', 'For the rare and radiant maiden\n', 'Whom the angels name Lenore—\n', 'Nameless here for evermore.\n', 'And the silken, sad, uncertain\n', 'Rustling of each purple curtain\n', 'Thrilled me,—filled me with fantastic\n', 'Terrors, never felt before;\n', 'So that now, to still the beating\n', 'Of my heart, I stood repeating,\n', '" \'T is some visitor entreating\n', 'Entrance at my chamber door\n', 'Some late visitor entreating\n', 'Entrance at my chamber door;\n', 'This it is and nothing more."\n', 'Presently my soul grew stronger;\n', 'Hesitating then no longer,\n', '"Sir," said I, "or Madam, truly\n', 'Your forgiveness I implore;\n', 'But the fact is I was napping,\n', 'And so gently you came rapping,\n', 'And so faintly you came tapping,\n', 'Tapping at my chamber door,\n', 'That I scarce was sure I heard you"—\n', 'Here I opened wide the door;\n', 'Darkness there and nothing more.\n', 'Deep into that darkness peering,\n', 'Long I stood there, wondering, fearing,\n', 'Doubting, dreaming dreams no mortals\n', 'Ever dared to dream before;\n', 'But the silence was unbroken,\n', 'And the stillness gave no token,\n', 'And the only word there spoken\n', 'Was the whispered word, "Lenore?"\n', 'This I whispered, and an echo\n', 'Murmured back the word, "Lenore!"—\n', 'Merely this and nothing more.\n', 'Back into the chamber turning,\n', 'All my soul within me burning,\n', 'Soon again I heard a tapping\n', 'Something louder than before.\n', '"Surely," said I, "surely, that is\n', 'Something at my window lattice;\n', 'Let me see, then, what thereat is,\n', 'And this mystery explore—\n', 'Let my heart be still a moment\n', 'And this mystery explore;—\n', "'T is the wind and nothing more."]

        #chartreuse3
        #mediumseagreen

        self.listbox = tkinter.Listbox(listvariable=self.__strippers(values().get_base_terminal_message()), background=self.background, font=("Better VCR", 12), foreground="springgreen3", activestyle="none")
        #self.listbox = tkinter.Listbox(listvariable=self.__strippers(data), background=self.background, font=("Better VCR", 12), foreground="springgreen3", activestyle="none")
        self.listbox.bind("<<ListboxSelect>>", lambda x: self.listbox.selection_clear(0, tkinter.END))
        self.listbox.pack(side="left", fill="both", expand=1)
        scrollbar = ttk.Scrollbar(orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox["yscrollcommand"] = scrollbar.set

        self.entry = tkinter.Text(relief="sunken", background=self.background, foreground="springgreen3", font=("Better VCR", 12), width=98, height=12, cursor="pencil")

        #self.entry.pack(side="left", fill="both", expand=1)
        self.entry.place(x=1, y=502)

        ROOT = root
        return root


