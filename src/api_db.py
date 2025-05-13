from connection import *


class API:
    def __init__(self):
        pass


    def selectall_where(self, db_name, value, table_name, column_name="*"):
        query = f"""SELECT {column_name} from {table_name} WHERE ?='?'"""
        with SQLiteDB (db_name) as db:
            db.execute(query, value)
            result = db.fetchall()
        return (row for row in result) if result else ()

    
    def selectall(self, db_name, value, table_name, column_name):
        query = f"""SELECT {column_name} FROM {table_name}"""
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
            

