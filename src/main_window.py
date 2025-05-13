import tkinter as tk
from tkinter import ttk
from tab_frame import *
# import manim

from api_db import *


class TkinterWindow(tk.Tk):
    # UI программы
    def __init__(self, title: str, resizable: tuple, size):
        super().__init__()
        self.win_title = title
        self.win_resizable = resizable
        self.size = size

        self.build_ui()

        self.mainloop()

    
    def setting_window_give(self):
        self.title(self.win_title)
        self.resizable(*self.win_resizable)
        # self.iconbitmap()

        # if self.size == "fullscreen": 
        #     self.state("zoomed")
        # else:
        self.geometry(f"{self.size[0]}x{self.size[1]}")

    
    def build_ui(self):
        self.setting_window_give()
        self.style_create()
        self.title_create()
        self.notebook_create()


    def style_create(self):
        style = ttk.Style()
        # для расстяжения вкладок
        self.update_idletasks()    
        style.configure('TNotebook.Tab',
                        padding=(0, 1),
                        stretch=True,
                        anchor="center",
                        width=self.winfo_width(),
                        font=('Bahnschrift SemiBold SemiConden', 18))

    
    def frame_for_notebook_create(self):
        self.frame_branch = BranchTab(self.notebook)
        self.frame_formula = FormulaTab(self.notebook)
        self.frame_output = OutputTab(self.notebook)

        self.frames_for_notebook = {self.frame_branch: "Разделы", 
                                   self.frame_formula: "Формула", 
                                   self.frame_output: "Вывод"}
                             

    def notebook_create(self):
        """
        Класс для создания и настройки вкладок
        """
        self.notebook = ttk.Notebook()
        self.notebook.pack(fill="both", expand=True)

        self.frame_for_notebook_create()
        
        for frame, title in self.frames_for_notebook.items():
            self.notebook.add(frame, text=title)


    def title_create(self):
        """
        Функция для создания заголовка
        """
        title_frame = ttk.Frame(self, height=100)
        title_frame.pack(fill="x")

        title_label = ttk.Label(title_frame, text="Формулатория", anchor="center", font=('Bahnschrift SemiBold SemiConden', 24))
        title_label.pack(pady=10)      

            

TkinterWindow("Очень крутая программа от Lamwarld", (False, False), (1200, 1000))