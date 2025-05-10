from db.connection import *
# from ui.main_ui import *

import tkinter as tk
from tkinter import ttk
# import manim


class TkinterWindow(tk.Tk):
    # UI программы
    def __init__(self, title: str, resizable: tuple, size: str):
        super().__init__()
        self.title = title
        self.resizable = resizable
        self.size = size

        self.setting_window_give()

        self.mainloop()

    
    def setting_window_give(self):
        self.title()
        self.resizable(*self.resizable)
        self.size(self.size)


TkinterWindow("test", (False, False), "1200x1200")