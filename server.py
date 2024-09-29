from flask import Flask, request, jsonify
import logging
import datetime
from user_controller import UserController
from sql_db import SQLiteDB
import jwt

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

SECRET_KEY = 'qwerty12345'

# Создаем экземпляр класса SQLiteDB
db = SQLiteDB()
users_controller = UserController(db)

@app.before_first_request
def initialize_database():
    """Инициализирует базы данных перед первым запросом."""
    db.init_db()
    logging.info("База данных инициализирована.")

@app.route('/login', methods=['POST'])
def login():
    login = request.json.get('login')
    password = request.json.get('password')

    users = users_controller.get_all_users()

    if login in users and users[login] == password:
        token = generate_token(login)
        logging.info(f"Пользователь {login} авторизовался.")
        return jsonify(access_token=token), 200

    logging.warning("Неверный логин или пароль.")
    return jsonify(message="Неверный логин или пароль."), 401

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

if __name__ == '__main__':
    app.run(debug=True)