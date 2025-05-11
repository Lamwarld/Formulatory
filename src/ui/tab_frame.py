import tkinter as tk
from tkinter import ttk

class FilterTab(ttk.Frame):
    """
    Класс для реализации вкладки 'Фильтр'
    """
    def __init__(self, master):
        super().__init__(master)
        self.build_ui()

    
    def build_ui(self):
        self.branch_selector_create()
        

    def branch_selector_create(self):
        self.label_branch = ttk.Label(self, text="Выберите раздел", font=("Bahnschrift SemiBold SemiConden", 16))
        self.label_branch.grid(row=0, column=0, padx=10, pady=10)

        self.combobox_branches = ttk.Combobox(self, height=50, width=60)
        self.combobox_branches.grid(row=1, column=0, padx=10, pady=10)


class FormulaTab(ttk.Frame):
    def __init__(self):
        super().__init__()
        self.build_ui()

    
    def build_ui(self):
        pass


class ManegementTab(ttk.Frame):
    def __init__(self):
        super().__init__()
        self.build_ui()

    
    def build_ui(self):
        pass
