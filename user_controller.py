import sqlite3
from hashlib import sha256
import json
from generators import generate_keys_json


class UserController:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Создание таблицы пользователей, если она не существует."""
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            signature TEXT
        )
        '''
        self.cursor.execute(query)
        self.connection.commit()

    def register_user(self, username, password):
        """Регистрация нового пользователя с созданием цифровой подписи."""
        if self.is_user_exist(username):
            return False, "Username already exists."

        password_hash = self.hash_password(password)
        digital_signature = generate_keys_json() # Генерация цифровой подписи
        query = "INSERT INTO users (username, password_hash, signature) VALUES (?, ?, ?)"
        try:
            self.cursor.execute(query, (username, password_hash, digital_signature))
            self.connection.commit()
            return True, "User registered successfully."
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def is_user_exist(self, username):
        """Проверка, существует ли пользователь."""
        query = "SELECT id FROM users WHERE username = ?"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone() is not None

    def login_user(self, username, password):
        """Вход пользователя."""
        password_hash = self.hash_password(password)
        query = "SELECT id FROM users WHERE username = ? AND password_hash = ?"
        self.cursor.execute(query, (username, password_hash))
        return self.cursor.fetchone() is not None

    def hash_password(self, password):
        """Хэширование пароля."""
        return sha256(password.encode()).hexdigest()

    def save_signature(self, username, signature):
        """Сохранение цифровой подписи пользователя."""
        query = "UPDATE users SET signature = ? WHERE username = ?"
        try:
            self.cursor.execute(query, (signature, username))
            self.connection.commit()
            return True, "Success"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def load_signature(self, username):
        """Загрузка цифровой подписи пользователя."""
        query = "SELECT signature FROM users WHERE username = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_signature_data(self, username):
        """Получение данных подписи пользователя."""
        query = "SELECT signature FROM users WHERE username = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        if result and result[0]:
            return json.loads(result[0])  # Десериализация данных подписи
        return None

    def __del__(self):
        self.connection.close()


