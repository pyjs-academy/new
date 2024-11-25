import sqlite3

def create_db():
    # Создание базы данных и таблицы пользователей, если она не существует
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def get_user(username):
    # Соединение с базой данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Запрос пользователя по имени
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {"id": user[0], "username": user[1], "password": user[2]}
    return None

def add_user(username, password):
    # Соединение с базой данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Добавление пользователя в базу данных
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
