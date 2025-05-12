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
        self.style_create()
        self.branch_selector_create()
        

    def branch_selector_create(self):
        self.label_branch = ttk.Label(self, text="Выберите раздел", font=("Bahnschrift SemiBold SemiConden", 16))
        self.label_branch.grid(row=0, column=0, padx=10, pady=10)

        val = ["jopa", "xui"]

        self.combobox_branches = ttk.Combobox(self, values=val, width=50, style="TCombobox", justify="center")
        self.combobox_branches.grid(row=1, column=0, padx=10, pady=10)

    
    def style_create(self):
        style = ttk.Style()
        self.option_add("*TCombobox.font", ("Arial", 16))
        self.option_add("*TCombobox*Listbox.font", ("Arial", 16))


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
