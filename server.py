from flask import Flask, request, jsonify, render_template
import logging
import datetime
from user_controller import UserController
from sql_db import SQLiteDB
from flask_jwt_extended import JWTManager, create_access_token
from drone_controller import DroneController

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, template_folder='templates', static_folder='static')


# Конфигурируем секретный ключ для JWT
app.config['SECRET_KEY'] = 'my_secret_key'
jwt = JWTManager(app)

# Простое хранилище токенов для авторизованных пользователей
user_tokens = {}

# Создаем экземпляр класса SQLiteDB
db = SQLiteDB()
users_controller = UserController(db)
drone_controller = DroneController(db)

def initialize_database():
    """Инициализирует базы данных."""
    db.init_db()
    logging.info("База данных инициализирована.")

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    login = request.json.get('username')
    password = request.json.get('password')

    users = users_controller.get_all_users()
    print(users)

    for user in users:
        if login in user and user[1] == login and user[4] == password:
            # Генерация JWT токена
            token = create_access_token(identity=login)
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Неверный логин или пароль"}), 401

@app.route("/home")
def main_page():
    drones_data = drone_controller.get_all_drones()
    drones = [
        dict(id=id, model=model, status=status)
        for id, model, status in drones_data
    ]
    return render_template("home.html", drones=drones)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)