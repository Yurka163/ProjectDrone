import logging
from db.Database import SQLiteDBFactory
from db.QueryBuilder import QueryBuilder
from dto.drone_dto import DroneDto


class DroneController:
    """Класс для работы с базой дронов"""
    @staticmethod
    def add(drone: DroneDto):
        """Метод добавляющий дрон в БД"""
        query_builder = QueryBuilder()
        conn = SQLiteDBFactory.get_db()
        query = query_builder.insert_into("tbl_drones", [
            "port",
            "serial_number",
            "mission",
            "created_at"
        ]).values(
            drone.port,
            drone.serial_number,
            drone.mission,
            drone.created_at
        ).build()
        conn.execute(query, query_builder.get_params())
        conn.commit()
        conn.close()
        logging.info(f"Дрон {drone.serial_number} сохранен в БД")

    @staticmethod
    def get_all():
        """Метод возвращает список всех дронов из БД"""
        query_builder = QueryBuilder()
        cursor = SQLiteDBFactory.get_db().cursor()
        drones = cursor.execute(query_builder.select("tbl_drones").build()).fetchall()
        cursor.close()
        return drones

    @staticmethod
    def get_one(id):
        query_builder = QueryBuilder()
        cursor = SQLiteDBFactory.get_db().cursor()
        select = query_builder.select("tbl_drones").where("id = ?", [id]).build()
        drones = cursor.execute(select, query_builder.get_params()).fetchall()
        cursor.close()
        return drones

    @staticmethod
    def update(drone: DroneDto):
        """Метод обновляющий статус миссии в телеметрии"""
        update_data = {
            'mission': drone.mission
        }
        query_builder = QueryBuilder()
        conn = SQLiteDBFactory.get_db()
        query = query_builder.update('tbl_drones').set(update_data).where("id = ?", [drone.id]).build()
        drones = conn.cursor().execute(query, query_builder.get_params())
        conn.commit()
        logging.info("Статус 'Миссия' обновлен.")
        conn.close()
        return drones


@staticmethod
def remove(user: DroneDto):
    pass
