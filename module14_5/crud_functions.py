import sqlite3
connection = sqlite3.connect('database.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL
    )
    ''')
    connection.commit()

def add_user(username, email, age):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', (username, email, age, 1000))
    connection.commit()

def is_included(username):
    check_users = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    if check_users.fetchone() is None:  # Правильная проверка на None
        return False
    else:
        return True


def get_all_products():
    cursor.execute('SELECT * FROM Users')
    products = cursor.fetchall()
    return products

