import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
from sys import exc_info
# import manim


class SQLiteDB():
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.enter = False


    def __enter__(self):
        # подключение к базе данных и создание курсора (работа с with)
        try:
            self.connection = sql.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.enter = True
            return self
        except:
            print(f"Произошла ошибка подключения к базе данных")
            self.__exit__(*exc_info())
            raise

    
    def __exit__(self, exc_type, exc_value, traceback):
        # закрываем подключение (окончание with) 
        if not self.enter:
            #Если подключение не удалось, то отключаем курсор и соединение
            if self.cursor:
                try:
                    self.cursor.close()
                except: 
                    print("Произошла ошибка при закрытии курсора")
            if self.connection:
                try:
                      self.connection.close()
                except:
                     print("Произошла ошибка при закрытии соединения")
            return   

        try: 
            if self.connection:
                if exc_type:
                    # если произошла ошибка во время выполнения команды
                    self.connection.rollback()
                    print("Произошла ошибка при выполнении команды")
                else:
                    self.connection.commit()
        except Exception as e:
            print(f"Произошла ошибка во время завершения команды")
        finally:
            try:
                if self.cursor:
                    self.cursor.close()
                if self.connection:
                    self.connection.close()
            except Exception as e:
                print(f"Произошла ошибка при закрытии базы данных")

        
    def execute(self, sql, params):
        """
        sql - сама команда с подстановками в виде '?'
        params - значения, которые подставятся вместо '?'
        """
        if not self.cursor:
            raise RuntimeError("Курсор не инициализирован")
        self.cursor.execute(sql, params)


    def fetchall(self):
        return self.cursor.fetchall()


    def fetchone(self):
        return self.cursor.fetchone()
