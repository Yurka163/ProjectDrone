from sql_db import SQLiteDB, QueryBuilder
from dto.user import User
import logging

class UserController:
    """Класс для работы с базой пользователей"""

    def __init__(self, db: SQLiteDB):
        self.db = db

    def add_user(self, user: User):
        """Метод добавляющий пользователя в БД"""
        query_builder = QueryBuilder()
        query = query_builder.insert_into("tbl_users", ["login",
                                                        "first_name", "last_name", "password"]).values(
            user._login, user._first_name, user._last_name, user._password).build()
        params = query_builder.get_params()
        try:
            with self.db.connect('users_db') as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute(query, params)
                    conn.commit()
                    logging.info(f"Пользователь {user._first_name} {user._last_name} успешно добавлен.")
        except Exception as e:
            logging.error(f"Ошибка при добавлении пользователя: {e}")

    def get_all_users(self):
        """Метод возвращает список всех пользователей из БД"""
        query_builder = QueryBuilder()
        with self.db.connect(path_to_db="database.db") as connection:
            cursor = connection.cursor()
            try:
                users = cursor.execute(query_builder.select("tbl_users").build()).fetchall()
            except Exception as e:
                logging.error(f"Ошибка при получении пользователей: {e}")
                users = []  # В случае ошибки возвращаем пустой список
        return users
