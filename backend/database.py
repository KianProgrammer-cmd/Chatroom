import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "chatroom.db")


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            room TEXT NOT NULL DEFAULT 'main',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def create_user(username, password):
    connection = get_connection()

    try:
        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_user(username):
    connection = get_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    connection.close()

    return user


def save_message(username, message, room="main"):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO messages (username, message, room)
        VALUES (?, ?, ?)
        """,
        (username, message, room)
    )

    connection.commit()
    connection.close()


def get_messages(room="main"):
    connection = get_connection()

    messages = connection.execute(
        """
        SELECT username, message, created_at
        FROM messages
        WHERE room = ?
        ORDER BY id ASC
        """,
        (room,)
    ).fetchall()

    connection.close()

    return messages