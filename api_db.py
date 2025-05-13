from connection import *


class APIFormula:
    def __init__(self):
        self.db_name = "formula.db"

    
    def execute_query(self, query, params):
        try:
            with SQLiteDB(self.db_name) as db:
                db.execute(query, params)
        except:
            print("Ошибка execute")


    def select_all(
        self,
        table: str,
        columns: str = "*",
        where: dict = None,
        order_by: str = None,
        limit: int = None):
        """
        Универсальный метод для SELECT-запросов.
        
        Параметры:
            - db_name: Имя базы данных.
            - table_name: Имя таблицы.
            - columns: Строка с именами столбцов (по умолчанию "*").
            - where: Словарь условий {column: value} (например, {"id": 5, "name": "John"}).
            - order_by: Строка для сортировки (например, "id DESC").
            - limit: Ограничение количества строк.
        
        Возвращает генератор строк (или пустой генератор, если нет данных).
        """
        query = f"SELECT {columns} FROM {table}"
        params = []

        # Динамическое добавление WHERE (если есть условия)
        if where:
            where_clause = " AND ".join(f"{col} = ?" for col in where.keys())
            query += f" WHERE {where_clause}"
            params.extend(where.values())

        # Добавляем сортировку (ORDER BY)
        if order_by:
            query += f" ORDER BY {order_by}"

        # Добавляем лимит (LIMIT)
        if limit:
            query += f" LIMIT {limit}"

        # Выполняем запрос
        with SQLiteDB(self.db_name) as db:
            db.execute(query, params)
            result = db.fetchall()

        return tuple(result) if result else ()
    

    def delete_branch(self, name):
        query = "DELETE FROM formula_category WHERE name = ?"
        return self.execute_query(query, (name,))


    def update_branch(self, new_name, old_name):
        query = """UPDATE formula_category SET name=? WHERE name=?"""
        self.execute_query(query, (new_name, old_name))


    def create_branch(self, name):
        query = """INSERT INTO formula_category ("name") VALUES (?)"""
        self.execute_query(query, (name,))
            

