import sqlite3
import logging
from abc import ABC, abstractmethod
from dto.user import UserDto
from query_builder import QueryBuilder

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DBFactory(ABC):
    """Абстрактный класс, представляющий фабрику для подключения к базе данных"""
    @abstractmethod
    def connect(self, path_to_db: str):
        pass

    @abstractmethod
    def close_connect(self, conn):
        pass


class SQLiteDB(DBFactory):
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

    def create_users_table(self):
        """Создает таблицу пользователей."""
        create_users_table_sql = """
            CREATE TABLE IF NOT EXISTS tbl_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,          
                last_name TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """
        self.create_table(path_to_db='database.db', create_table_sql=create_users_table_sql)

    def create_drones_table(self):
        """Создает базу данных дронов."""
        create_drones_table_sql = """
            CREATE TABLE IF NOT EXISTS tbl_drones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL          
            )
        """
        self.create_table(path_to_db='database.db', create_table_sql=create_drones_table_sql)

    def init_db(self):
        """Инициализирует базы данных и создает необходимые таблицы."""
        self.create_users_table()
        self.create_drones_table()
        self.create_admin_user()

    def create_admin_user(self):

        query_builder = QueryBuilder()
        user = UserDto(login="admin", first_name="admin", last_name="admin", password="admin")

        # Проверка на существование администратора
        conn = self.connect("database.db")
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tbl_users WHERE login=?", (user.login,))
            exists = cursor.fetchone()[0]

            if exists:
                logging.info("Администратор уже существует.")
                self.close_connect(conn)
                return

            columns = ['login', 'first_name', 'last_name', 'password']
            values = [user.login, user.first_name, user.last_name, user.password]

            query = query_builder.insert_into("tbl_users", columns).values(*values).build()

            try:
                cursor.execute(query, query_builder.get_params())
                conn.commit()
                logging.info("Администратор успешно создан.")
            except sqlite3.Error as e:
                logging.error(f"Ошибка при создании администратора {e}.")
