import sqlite3
import logging
from typing import Optional, List

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class SQLiteDB:
    """Класс для работы с базой данных SQLite."""

    def connect(self, path_to_db: str):
        """
        Подключается к базе данных SQLite.
        Передается путь к файлу базы данных.
        Возвращает объект соединения или None в случае ошибки.
        """
        try:
            # Подключение к базе данных SQLite
            conn = sqlite3.connect(path_to_db)
            logging.info(f"Подключение к БД установлено")
            return conn
        except sqlite3.Error as e:
            # Обработка ошибки подключения
            logging.warning(f"Ошибка подключения: {e}")
            return None

    def close_connect(self, conn):
        """
        Закрывает соединение с базой данных.
        Передается объект соединения, который необходимо закрыть.
        """
        if conn:
            conn.close()
            logging.info("Соединение с БД закрыто")

    def create_table(self, path_to_db: str, create_table_sql: str):
        """
        Создает таблицу в базе данных SQLite.

        Передается имя файла базы данных.
        Передается SQL-запрос для создания таблицы.
        """
        conn = self.connect(path_to_db=path_to_db)
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(create_table_sql)
                logging.info("Таблица успешно создана")
            except sqlite3.Error as e:
                logging.error(f"Ошибка создания таблицы: {e}")
            finally:
                self.close_connect(conn)

    def create_users_db(self):
        """Создает базу данных пользователей."""
        create_users_table_sql = """
            CREATE TABLE IF NOT EXISTS tbl_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,          
                last_name TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """
        self.create_table(db_name='users_db', create_table_sql=create_users_table_sql)

    def create_drones_db(self):
        """Создает базу данных дронов."""
        create_drones_table_sql = """
            CREATE TABLE IF NOT EXISTS tbl_drones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL          
            )
        """
        self.create_table(db_name='drones_db', create_table_sql=create_drones_table_sql)

    def init_db(self):
        """Инициализирует базы данных и создает необходимые таблицы."""
        self.create_users_db()
        self.create_drones_db()


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
