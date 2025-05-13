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
        self.api_db = APIFormula()
        
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
            data = self.api_db.select_all(columns="name", table="formula_category")

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
            name = self.entry.get()
            if not name:
                messagebox.showerror("Ошибка!", "Введите название раздела")
                return
    
        
            if self.api_db.select_all(table="formula_category", where={"name": name}):
                messagebox.showerror("Ошибка!", "Такой раздел уже существует")
                return
                
            self.api_db.create_branch(name)
            self.entry.delete(0, "end")
            self.__update_treeview()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать категорию: {str(e)}")
        

    def __category_update(self): 
        try:
            new_name = self.entry.get().strip()
        
            # Проверка на пустое поле
            if not new_name:
                messagebox.showerror("Ошибка!",  message="Название раздела не может быть пустым")
                return
                
            # Проверка, что старое имя существует
            if not self.old_name_selected_branch:
                messagebox.showerror("Ошибка!", message="Не выбран раздел для изменения")
                return
                
            # Проверка, что новое имя не совпадает со старым
            if new_name == self.old_name_selected_branch:
                messagebox.showinfo("Информация", message="Такой раздел уже существует")
                return
                
            # Проверка существования нового имени
            existing = self.api_db.select_all(columns="name", 
                                            table="formula_category",
                                            where={"name": new_name})
                                            
            
            if existing:
                messagebox.showerror("Ошибка!", message=f"Раздел '{new_name}' уже существует")
                return

            if not messagebox.askyesno("Внимание!", message="Раздел будет изменён", 
                                       detail=f"Изменить раздел {self.old_name_selected_branch}' на '{new_name}'?"):
                return
            self.api_db.update_branch(self.entry.get(), self.old_name_selected_branch)
            self.__update_treeview()   

        except sql.Error as e:
            messagebox.showerror("Ошибка БД!", message=f"Произошла ошибка во время \n изменения раздела \n{e}")
        
        except Exception as e:
            messagebox.showerror("Ошибка", message=f"Неизвестная ошибка \n{e}")


    def __category_delete(self):
        try:
            if not self.old_name_selected_branch:
                messagebox.showerror("Ошибка!", message="Не выбран раздел для удаления")
                return
            
            if not messagebox.askyesno("Внимание!", message="Раздел будет удалён!", 
                                       detail=f"Удалить раздел {self.old_name_selected_branch}?"):
                return
            self.api_db.delete_branch(self.old_name_selected_branch)
            self.__update_treeview()   

        except sql.Error as e:
            messagebox.showerror("Ошибка БД!", message=f"Произошла ошибка во время \n удаления раздела \n{e}")
        
        except Exception as e:
            messagebox.showerror("Ошибка", message=f"Неизвестная ошибка \n{e}")


class FormulaTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.api_db = APIFormula()
        self.build_ui()

    
    def build_ui(self):
        self.__style_create()
        self.__combobox_create()
        self.__scrolled_treeview_create()


    def __style_create(self):
        style = ttk.Style()

        self.option_add("*TCombobox.font", ("Arial", 16))
        self.option_add("*TCombobox*Listbox.font", ("Arial", 16))
        
        self.grid_columnconfigure(1, weight=1)


    def __combobox_create(self):
        try:
            self.label_branch = ttk.Label(self, text="Выберите раздел", font=("Arial", 16))
            self.label_branch.grid(row=0, column=0, padx=10, pady=10)

            branches = self.api_db.select_all(columns="name", table="formula_category")
            branches = [val[0] for val in branches if val]

            self.branch_combobox = ttk.Combobox(self, values=branches, width=40, state="readonly")
            self.branch_combobox.grid(row=1, column=0, padx=10, pady=10)
        except:
            self.branch_combobox = ttk.Combobox(self, values=["Ошибка загрузки"], width=40, state="disabled")
        


    def __scrolled_treeview_create(self):
        scrolled_frame = ttk.Frame(self)
        scrolled_frame.grid(row=2, column=0, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(scrolled_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        treeview_formula = ttk.Treeview(
            scrolled_frame,
            columns=("branch", "name", "formula"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        treeview_formula.pack(expand=True, fill="both")

        scrollbar.config(command=treeview_formula.yview)

        treeview_formula.heading("branch", text="Раздел")
        treeview_formula.heading("name", text="Название")
        treeview_formula.heading("formula", text="Формула")
        treeview_formula.column("branch", width=150)
        treeview_formula.column("name", width=150)
        treeview_formula.column("formula", width=150)


class OutputTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.build_ui()

    
    def build_ui(self):
        pass
