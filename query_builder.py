from typing import Optional, List


class QueryBuilder:
    """Класс для построения SQL-запросов с использованием паттерна 'Builder' и 'Singleton'"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(QueryBuilder, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Инициализирует экземпляр QueryBuilder с пустыми частями запроса и параметрами."""
        if not hasattr(self, 'initialized'):  # Проверка на инициализацию
            self.initialized = True
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

    def values(self, *columns):
        """
        Добавляет значения для вставки в запрос.
        Передаются значения, которые будут вставлены в соответствующие столбцы.
        Возвращает экземпляр QueryBuilder для дальнейшего построения запроса.
        """
        self.__params.extend(columns)
        return self

    def get_params(self):
        """Метод для получения списка параметров"""
        return self.__params

    def select(self, table: str, columns="*"):
        """Метод для создания части запроса SELECT"""
        self.__query_parts["SELECT"] = f"SELECT {columns}"
        self.__query_parts["FROM"] = f"FROM {table}"
        return self

    def where(self, condition: str, params: Optional[List] = None):
        """Метод для добавления условия к SQL-запросу"""
        self.__query_parts["WHERE"] = f"WHERE {condition}"
        if params is not None:
            self.__params.extend(params)
        return self

    def reset(self):
        """Сбрасывает состояние QueryBuilder."""
        self.__query_parts.clear()
        self.__params.clear()

    def build(self):
        """Строит итоговый SQL-запрос."""
        query = ""
        if "INSERT INTO" in self.__query_parts:
            query = self.__query_parts["INSERT INTO"]
        if "SELECT" in self.__query_parts:
            query = f'{self.__query_parts["SELECT"]} {self.__query_parts["FROM"]} '
        if "WHERE" in self.__query_parts:
            query += self.__query_parts["WHERE"]
        return query
