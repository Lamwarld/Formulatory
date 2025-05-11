import tkinter as tk
from tkinter import ttk
# import manim


class TkinterWindow(tk.Tk):
    # UI программы
    def __init__(self, title: str, resizable: tuple, size):
        super().__init__()
        self.win_title = title
        self.win_resizable = resizable
        self.size = size

        self.build_ui()
        self.configure_style()

        self.mainloop()

    
    def setting_window_give(self):
        self.title(self.win_title)
        self.resizable(*self.win_resizable)
        # self.iconbitmap()

        if self.size == "fullscreen": 
            self.state("zoomed")
        else:
            self.geometry(f"{self.size[0]}x{self.size[1]}")

    
    def configure_style(self):
        style = ttk.Style()
        # style.configure('TNotebook.Tab', padding=(20, 5), stretch=True)  # Растягиваем вкладки

    
    def build_ui(self):
        self.setting_window_give()
        self.notebook_create()

    
    def frame_for_notebook_create(self):
        self.frame_filter = ttk.Frame(self.notebook)
        self.frame_formula = ttk.Frame(self.notebook)
        self.frame_management = ttk.Frame(self.notebook)

        self.frames_for_notebook = {self.frame_filter: "Фильтр", 
                                   self.frame_formula: "Формула", 
                                   self.frame_management: "Управление"}
        
    
    def style_for_notebook_create(self):
        style = ttk.Style()
        # для расстяжения вкладок
        self.update_idletasks()    
        style.configure('TNotebook.Tab',
                        padding=(0, 1),
                        stretch=True,
                        anchor="center",
                        width=self.winfo_width(),
                        font=('Bahnschrift SemiBold SemiConden', 18))
                        

    def notebook_create(self):
        self.notebook = ttk.Notebook()
        self.notebook.pack(fill="both", expand=True)

        self.frame_for_notebook_create()
        self.style_for_notebook_create()
        
        for frame, title in self.frames_for_notebook.items():
            self.notebook.add(frame, text=title)


    # def 
            

TkinterWindow("test", (False, False), "fullscreen")