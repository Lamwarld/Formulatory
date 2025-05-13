import tkinter as tk
from tkinter import ttk

from api_db import *


class BranchTab(ttk.Frame):
    """
    Класс для реализации вкладки 'Фильтр'
    """
    def __init__(self, master):
        super().__init__(master)
        self.api_db = API()
        self.build_ui()

    
    def build_ui(self):
        self.style_create()
        self.treeview_create()
        self.create_CRUD_entry()

    
    def style_create(self):
        style = ttk.Style()
        self.option_add("*TCombobox.font", ("Arial", 16))
        self.option_add("*TCombobox*Listbox.font", ("Arial", 16))


    def treeview_create(self):
        self.branch_treeview = ttk.Treeview(self, columns=["branch"], show="headings", style="Treeview")
        self.branch_treeview.heading("branch", text="Раздел")
        self.branch_treeview.column("branch", width=300, anchor="center")

        self.branch_treeview.grid(row=0, column=0, padx=10, pady=10)

        self.update_treeview()


    def update_treeview(self, data=None):
        self.branch_treeview.delete(*self.branch_treeview.get_children())

        if data is None:
            data = self.api_db.select_category()

        for row in data:
            self.branch_treeview.insert("", "end", values=(row))

    
    def create_CRUD_entry(self):
        self.user_input = tk.StringVar()

        self.label_CRUD = ttk.Label(self, 
                                    text="Введите для изменения, добавления или удаления", 
                                    font=("Arial", 15))
        self.label_CRUD.grid(row=1, column=0, padx=10, pady=20)
        
        self.entry = ttk.Entry(self, textvariable=self.user_input, width=40, font=("Arial", 16))
        self.entry.grid(row=2, column=0, padx=10, pady=10)
        


class FormulaTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.build_ui()

    
    def build_ui(self):
        pass


class OutputTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.build_ui()

    
    def build_ui(self):
        pass
