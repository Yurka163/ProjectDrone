from sql_db import SQLiteDB
from query_builder import QueryBuilder
from dto.drone import DroneDto
import logging


class DroneController:
    """Класс для работы с базой дронов"""

    def __init__(self, db: SQLiteDB):
        self.db = db

    def add_drone(self, drone: DroneDto):
        """Метод добавляющий дрон в БД"""
        query_builder = QueryBuilder()
        query = query_builder.insert_into("tbl_drones", ["model",
                                                         "status"]).values(
            drone.id, drone.status).build()
        params = query_builder.get_params()
        try:
            with self.db.connect('database.db') as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute(query, params)
                    conn.commit()
                    logging.info(f"Дрон {drone.model} успешно добавлен.")
        except Exception as e:
            logging.error(f"Ошибка при добавлении дрона: {e}")

    def get_all_drones(self):
        """Метод возвращает список всех дронов из БД"""
        query_builder = QueryBuilder()
        with self.db.connect(path_to_db="database.db") as connection:
            cursor = connection.cursor()
            try:
                drones = cursor.execute(query_builder.select("tbl_drones").build()).fetchall()
            except Exception as e:
                logging.error(f"Ошибка при получении списка дронов: {e}")
                drones = []  # В случае ошибки возвращаем пустой список
        return drones
