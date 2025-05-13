import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from api_db import *


class BranchTab(ttk.Frame):
    """
    Класс для реализации вкладки 'Фильтр'
    """
    def __init__(self, master):
        super().__init__(master)
        self.api_db = API()
        
        self.old_name_selected_branch = ''
        self.selected_branch = tk.StringVar(); self.selected_branch.set("Сейчас выбрано: ")

        self.__build_ui()

    
    def __build_ui(self):
        self.__style_create()
        self.__treeview_create()
        self.__create_CRUD()

    
    def __style_create(self):
        style = ttk.Style()
        
        self.grid_columnconfigure(1, weight=1)

        self.option_add("*TCombobox.font", ("Arial", 16))
        self.option_add("*TCombobox*Listbox.font", ("Arial", 16))

        style.configure("TButton", font=("Arial", 16))


    def __treeview_create(self):
        self.branch_treeview = ttk.Treeview(self, columns=["branch"], show="headings", style="Treeview")
        self.branch_treeview.heading("branch", text="Раздел")
        self.branch_treeview.column("branch", width=500, anchor="center")

        self.branch_treeview.grid(row=0, column=0, padx=10, pady=10)

        self.branch_treeview.bind("<<TreeviewSelect>>", lambda event: self.select_branch_row())

        self.__update_treeview()


    def __update_treeview(self, data=None):
        self.branch_treeview.delete(*self.branch_treeview.get_children())

        if data is None:
            data = self.api_db.select_all("formulatory.db", columns="name", table="formula_category")

        for row in data:
            self.branch_treeview.insert("", "end", values=row)

    
    def select_branch_row(self):
        for row in self.branch_treeview.selection():
            self.selected_branch.set(f'Сейчас выбрано: {self.branch_treeview.item(row)["values"][0]}')

            self.old_name_selected_branch = self.branch_treeview.item(row)["values"][0]

    
    def __create_CRUD(self):
        self.label_CRUD = ttk.Label(self, 
                                    text="Введите для изменения, добавления", 
                                    font=("Arial", 16))
        self.label_CRUD.grid(row=1, column=1, padx=10, pady=20)

        self.label_selected_branch = ttk.Label(self, textvariable=self.selected_branch, font=("Arial", 16))
        self.label_selected_branch.grid(row=1, column=0, padx=10, pady=10)

        self.entry = ttk.Entry(self, width=40, font=("Arial", 16))
        self.entry.grid(row=2, column=1, padx=10, pady=10)

        self.__create_CRUD_button()

    
    def __create_CRUD_button(self):
        button_frame = ttk.Frame(self)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid(row=0, column=1, sticky="we", padx=10, pady=10)

        button_frame.columnconfigure(0, weight=1)
        button_frame.rowconfigure(0, weight=1)

        self.button_create = ttk.Button(button_frame, text="Добавить", command=lambda: self.__category_create())
        self.button_update = ttk.Button(button_frame, text="Изменить", command=lambda: self.__category_update())
        self.button_delete = ttk.Button(button_frame, text="Удалить", command=lambda: self.__category_delete())

        buttons = (self.button_create, self.button_update, self.button_delete)
        for button in buttons:
            button.pack(side="top", fill="x", expand=True, pady=20, padx=10)  

    
    def __category_create(self):
        try:
            value = self.entry.get()
            """Нужно добавить проверку на существование"""
            if value:
                self.api_db.create_category("formulatory.db", (value,))
                self.entry.delete(0, "end")
                self.__update_treeview()
            else:
                messagebox.showerror(title="Ошибка!", message="Произошла ошибка во время \n добавления категории", icon="error", detail="Вы ничего не ввели")
        except:
            messagebox.showerror(title="Ошибка!", message="Произошла ошибка во время \n добавления категории", icon="error", detail="Ничего не было добавлено")
        

    def __category_update(self):
        try:
            if self.entry.get() == "":
                messagebox.showerror("Ошибка!", icon="error", message="Произошла ошибка во время \n изменения категории", detail="Раздел не выбран!")
            else:
                branch_is_exist = self.api_db.select_all("formulatory.db", columns="name", table="formula_category",
                                                          where={"name": self.old_name_selected_branch}) 
                                                            
                if len(branch_is_exist) == 0:
                    messagebox.showerror("Ошибка!", icon="error", message="Произошла ошибка во время \n изменения категории", detail="Такого раздела не существует")
                else:
                    value = self.entry.get()
                    branch_already_exist = self.api_db.select_all("formulatory.db", columns="name", table="formula_category",
                                                                  where={"name": value})
                                                                        
                    
                    if len(branch_already_exist) > 0:
                        messagebox.showerror("Ошибка!", icon="error", message="Произошла ошибка во время \n изменения категории", detail="Такой раздел уже существует")
                    else:
                        choice = messagebox.askyesno("Внимание!", message="Раздел был изменён?", detail="Вы уверены?")

                        if choice:
                            self.api_db.update_category((self.old_name_selected_branch, self.entry.get()))
                            self.__update_treeview()        
        except:
            messagebox.showerror("Ошибка!", icon="error", message="Произошла ошибка во время \n изменения категории")

    def __category_delete(self):
        pass


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
