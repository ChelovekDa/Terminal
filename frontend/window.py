import tkinter
from backend.preFiles.app.for_start import start

root = tkinter.Tk()
root["bg"] = "black"
root.title("HCC PROD. | Discord: english_horoshiy | TERMINAL")
w = 700
h = 400
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.resizable(width=False, height=False)

CordSetButton = tkinter.Button(text="Нажмите чтобы установить кнопку ")
CordLabel = tkinter.Label()

root.mainloop()
