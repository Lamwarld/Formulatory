from connection import *


class API:
    def __init__(self):
        pass


    def select_all(
        self,
        db_name: str,
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
        with SQLiteDB(db_name) as db:
            db.execute(query, params)
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
            

