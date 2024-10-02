# Паттерн Строитель для построения SQL-запросов
class QueryBuilder:
    """Класс для построения SQL-запросов с использованием паттерна 'Builder'"""
    def __init__(self):
        """Инициализирует экземпляр QueryBuilder с пустыми частями запроса и параметрами."""
        self.__query_parts = {}
        self.__params = []

    def insert_into(self, table: str, columns: list):
        """
        Создает часть SQL-запроса для вставки данных в указанную таблицу.
        Передается имя таблицы, в которую будут вставлены данные.
        Передается список имен столбцов, в которые будут вставлены значения.
        Возвращает экземпляр QueryBuilder для дальнейшего построения запроса.
        """
        cols = ','.join(columns)
        question_marks = ','.join(['?'] * len(columns))
        self.__query_parts["INSERT INTO"] = f"INSERT INTO {table} ({cols}) VALUES ({question_marks})"
        return self

    def values(self, *columns: list):
        """
        Добавляет значения для вставки в запрос.
        Передаются значения, которые будут вставлены в соответствующие столбцы.
        Возвращает экземпляр QueryBuilder для дальнейшего построения запроса.
        """
        self.__params.extend(columns)
        print(self.get_params())
        return self

    def get_params(self):
        """Метод для получения списка параметров"""
        return self.__params

    def select(self, table: str, columns="*"):
        """Метод для создания части запроса SELECT"""
        self.__query_parts["SELECT"] = f"SELECT {columns}"
        self.__query_parts["FROM"] = f"FROM {table}"
        return self

    def where(self, condition: str, params=None):
        """Метод для добавления условия к SQL-запросу"""
        self.__query_parts["WHERE"] = f"WHERE {condition}"
        if params:
            self.__params.extend(params)
        return self

    def update(self, table: str):
        """Метод для создания части запроса UPDATE"""
        self.__query_parts["UPDATE"] = f"UPDATE {table} SET"
        return self

    def set(self, columns: dict):
        """Метод для установки столбцов и их новых значений"""
        set_clause = ', '.join([f" {column} = ?" for column in columns.keys()])
        self.__query_parts["SET"] = set_clause
        self.__params.extend(columns.values())  # Add the values in the same order
        return self

    def build(self):
        """Строит итоговый SQL-запрос."""
        query = ""
        if "UPDATE" in self.__query_parts:
            query = self.__query_parts["UPDATE"]
        if "SET" in self.__query_parts:
            query += self.__query_parts["SET"]
        if "INSERT INTO" in self.__query_parts:
            query = self.__query_parts["INSERT INTO"]
        if "SELECT" in self.__query_parts:
            query = f'{self.__query_parts["SELECT"]} {self.__query_parts["FROM"]} '
        if "WHERE" in self.__query_parts:
            query += self.__query_parts["WHERE"]
        return query
