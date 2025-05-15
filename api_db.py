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
        table,
        columns: str = "*",
        where: dict = None,
        order_by: str = None,
        limit: int = None,
        join_conditions: list = None,
        join_type: str = "INNER"):
        """
        Универсальный метод для SELECT-запросов.
        
        Параметры:
            - db_name: Имя базы данных.
            - table_name: Имя таблицы.
            - columns: Строка с именами столбцов (по умолчанию "*").
            - where: Словарь условий {column: value} (например, {"id": 5, "name": "John"}).
            - order_by: Строка для сортировки (например, "id DESC").
            - limit: Ограничение количества строк.
            - join_type: Тип соединения (INNER, LEFT, RIGHT, FULL) - по умолчанию INNER
            - join_conditions: Список условий соединения (например, ["table1.id = table2.table1_id"])
        
        Возвращает генератор строк (или пустой генератор, если нет данных).
        """
        if isinstance(table, str):
            table = [table]

        query = f"SELECT {columns} FROM {table[0]}"
        params = []

        if join_conditions and isinstance(table, list):
            for i in range(1, len(table)):
                query += f" {join_type} JOIN {table[i]} ON {join_conditions[i-1]}"

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