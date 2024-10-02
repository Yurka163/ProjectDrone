import logging

from db.Database import SQLiteDBFactory
from db.QueryBuilder import QueryBuilder
from dto.user_dto import UserDto


class UserController:

    @staticmethod
    def add(user: UserDto):
        """Метод добавляющий пользователя в БД"""
        query_builder = QueryBuilder()
        query_builder.insert_into("tbl_users", list(vars(user).values())).build()
        logging.info("Пользователь добавлен.")

    @staticmethod
    def get_all():
        """Метод возвращает список всех пользователей из БД"""
        query_builder = QueryBuilder()
        cursor = SQLiteDBFactory.get_db().cursor()
        users = cursor.execute(query_builder.select("tbl_users").build()).fetchall()
        cursor.close()
        return users

    @staticmethod
    def remove(user: UserDto):
        pass
