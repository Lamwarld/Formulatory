import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from api_db import *
# from manim_renderer import *


class BranchTab(ttk.Frame):
    """
    Класс для реализации вкладки 'Фильтр'
    """
    def __init__(self, master):
        super().__init__(master)
        self.api_db = APIFormula()
        self.formula_tab = FormulaTab(master)
        
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
        
        self.formula_tab.combobox_update()

    
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
        self.current_image = None

        self.build_ui()

    
    def build_ui(self):
        self.frame_create()
        self.__style_create()
        self.__combobox_create()
        self.__scrolled_treeview_create()
        self.__add_reset_button()
        self.__formula_frame_label()


    def __style_create(self):
        style = ttk.Style()

        self.option_add("*TCombobox.font", ("Arial", 16))
        self.option_add("*TCombobox*Listbox.font", ("Arial", 16))
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.formula_frame.grid_rowconfigure(0, weight=1)
        self.formula_frame.grid_columnconfigure(0, weight=1)
        self.formula_frame2.grid_rowconfigure(0, weight=1)
        self.formula_frame2.grid_columnconfigure(0, weight=1)

    
    def frame_create(self):
        self.scrolled_frame = ttk.Frame(self)
        self.formula_frame = ttk.Frame(self)
        self.formula_frame2 = ttk.Frame(self)
        self.filter_frame = ttk.Frame(self)

        self.filter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self.scrolled_frame.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        self.formula_frame2.grid(row=2, column=0, padx=10, pady=10, sticky="we")
        self.formula_frame.grid(row=3, column=0, padx=10, pady=10, sticky="we")


    def __combobox_create(self):
        try:
            self.label_branch = ttk.Label(self.filter_frame, text="Выберите раздел", font=("Arial", 16))
            self.label_branch.grid(row=0, column=0, padx=10, pady=10)

            branches = self.api_db.select_all(columns="name", table="formula_category")
            branches = [val[0] for val in branches if val]

            self.branch_combobox = ttk.Combobox(self.filter_frame, values=branches, width=40, state="readonly")
            self.branch_combobox.grid(row=1, column=0, padx=10)

            self.branch_combobox.bind("<<ComboboxSelected>>", lambda event: self.__update_treeview())
        except:
            self.branch_combobox = ttk.Combobox(self.filter_frame, values=["Ошибка загрузки"], width=40, state="disabled")
        

    def combobox_update(self):
        branches = self.api_db.select_all(columns="name", table="formula_category")
        branches = [val[0] for val in branches if val]
        self.branch_combobox.config(values=branches)
        self.branch_combobox.set("")


    def __scrolled_treeview_create(self):
        scrollbar = ttk.Scrollbar(self.scrolled_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.treeview_formula = ttk.Treeview(
            self.scrolled_frame,
            columns=("branch", "name", "formula"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        self.treeview_formula.pack(expand=True, fill="both")

        scrollbar.config(command=self.treeview_formula.yview)

        self.treeview_formula.heading("branch", text="Раздел")
        self.treeview_formula.heading("name", text="Название")
        self.treeview_formula.heading("formula", text="Формула")
        self.treeview_formula.column("branch", width=100)
        self.treeview_formula.column("name", width=500)
        self.treeview_formula.column("formula", width=200)

        self.treeview_formula.bind("<<TreeviewSelect>>",lambda e: self.__on_formula_select())

        self.__update_treeview()


    def __add_reset_button(self):
        """Добавляет кнопку для сброса фильтра"""
        self.reset_button = ttk.Button(
            self.filter_frame,
            text="Сбросить фильтр",
            command=self.__reset_filter
        )
        self.reset_button.grid(row=1, column=1, padx=10, sticky="we")


    def __reset_filter(self):
        """Сбрасывает выбранный фильтр и обновляет TreeView"""
        self.branch_combobox.set('')  # Очищаем выбранное значение
        self.__update_treeview()  # Обновляем данные без фильтра


    def __update_treeview(self, data=None):
            self.treeview_formula.delete(*self.treeview_formula.get_children())
            branch = self.branch_combobox.get()

            try:
                data = self.api_db.select_all(
                    table=["formula", "formula_category"],
                    columns="formula.name, formula.expression, formula_category.name",
                    join_conditions=["formula.id_formula_category = formula_category.id"],
                    where={"formula_category.name": branch} if branch else None
                )
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить формулы: {str(e)}")

            for row in data:
                name = row[0]
                expresssion = row[1]
                branch_row = row[2]
                self.treeview_formula.insert("", "end", values=(branch_row, name, expresssion))


    def __formula_frame_label(self):
        self.formula_name = ttk.Label(self.formula_frame2, font=("Arial", 15, "bold"))
        self.formula_name.grid(row=0, column=0)

        self.formula_short_desc = ttk.Label(self.formula_frame2, font=("Arial", 15))
        self.formula_short_desc.grid(row=1, column=0)

        self.image_label = ttk.Label(self.formula_frame, anchor="center")
        self.image_label.grid(row=0, column=0, sticky="news")  


    def __formula_frame_create(self, formula_name):
        try:
            data = self.api_db.select_all(
                table="formula",
                columns="name, short_desc",
                where={"name": formula_name}
            )     
        except Exception as e:
            messagebox.showerror("Ошибка", "Оишбка во время загрузки названия и короткого описания формулы")

        except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить формулы: {str(e)}")

        for row in data:
            self.formula_name.config(text=f"{row[0]}")
            self.formula_short_desc.config(text=f"{row[1]}")

        
    def __on_formula_select(self):
        selected_item = self.treeview_formula.selection()
        if selected_item:
            item = self.treeview_formula.item(selected_item)
            formula_name = item['values'][1]  # колонка "name"

        # Пусть папка с изображениями называется 'images'
        images_dir = 'images'
        filename = f"{formula_name}.jpg"  # или другой формат, если нужно
        image_path = os.path.join(images_dir, filename)

        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)

                # Задаем максимальные размеры для отображения
                max_width, max_height = 400, 300  # например, 400x300

                # Вычисляем коэффициент масштабирования
                original_width, original_height = img.size
                scale_width = max_width / original_width
                scale_height = max_height / original_height
                scale = min(scale_width, scale_height, 1)  # не увеличиваем

                # Вычисляем новые размеры
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)

                # Масштабируем изображение
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Создаем PhotoImage
                self.current_image = ImageTk.PhotoImage(img_resized)
                self.__formula_frame_create(formula_name)
                self.image_label.config(image=self.current_image, text='')  # очищаем текст
            except Exception as e:
                print(f"Ошибка загрузки изображения: {e}")
                self.image_label.config(image='', text="Ошибка отображения изображения")
        else:
            # Если файла нет
            self.image_label.config(image='', text="Изображение не найдено")


    # def __on_formula_select(self):
    #     selected = self.treeview_formula.selection()
    #     if not selected:
    #         return
        
    #     item = self.treeview_formula.item(selected[0])
    #     formula = item["values"][2]

    #     self.__display_formula_image(formula)

    
    # def __display_formula_image(self, formula):
    #     for widget in self.formula_frame.winfo_children():
    #         widget.destroy()

    #     try:
    #         img = self.renderer.render_formula_to_image(formula)
    #         if img is None:
    #             raise ValueError("Не удалось сгенерировать изображение формулы")
            
    #         # Масштабируем изображение
    #         img = img.resize((600, 200), Image.LANCZOS)
    #         photo = ImageTk.PhotoImage(img)
            
    #         # Сохраняем ссылку, чтобы изображение не удалилось сборщиком мусора
    #         self.current_image = photo
            
    #         # Создаем Label для отображения формулы
    #         formula_label = ttk.Label(self.formula_frame, image=photo)
    #         formula_label.pack(pady=20, padx=20, fill="both", expand=True)
            
    #     except Exception as e:
    #         error_label = ttk.Label(
    #             self.formula_frame, 
    #             text=f"Ошибка отображения формулы:\n{str(e)}",
    #             foreground="red"
    #         )
    #         error_label.pack(pady=20)


class OutputTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.build_ui()

    
    def build_ui(self):
        pass
