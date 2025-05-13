from connection import *


class API:
    def __init__(self):
        pass

    
    def select_category(self):
        query = "SELECT name FROM formula_category"
        with SQLiteDB("formulatory.db") as db:
            db.execute(query, ())
            result = db.fetchall()
        return (row[0] for row in result) if result else ()
    

