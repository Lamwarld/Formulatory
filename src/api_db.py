from connection import *


class API:
    def __init__(self):
        pass


    def selectall_where(self, db_name, value):
        query = """SELECT * from ? WHERE ?='?'"""
        with SQLiteDB (db_name) as db:
            db.execute(query, value)
            result = db.fetchall()
        return (row for row in result) if result else ()

    
    def select(self, db_name, value):
        query = """SELECT ? FROM ?"""
        with SQLiteDB(db_name) as db:
            db.execute(query, value)
            result = db.fetchall()
        return (row for row in result) if result else ()
    

    def delete_category(self, db_name):
        pass


    def update_category(self, value):
        query = """UPDATE formula_category SET name=? WHERE name=?"""
        with SQLiteDB("formulatory.db") as db:
            db.execute(query, value)


    def create_category(self, db_name, value):
        query = """INSERT INTO formula_category("name") VALUES(?)"""
        with SQLiteDB(db_name) as db:
            db.execute(query, value)
            

