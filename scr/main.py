import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
# import manim


class SQLiteConnect():
    def __init__(self, db_name):
        self.connect_db = sql.connect("../formulatory.db")
        