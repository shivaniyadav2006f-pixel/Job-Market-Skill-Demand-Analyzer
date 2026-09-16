import sqlite3
import hashlib

DB_NAME = "users.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT DEFAULT ''
        )
    """)

    # Old database compatibility
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]

    if "email" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT DEFAULT ''")

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password, email=""):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password, email)
            VALUES (?, ?, ?)
            """,
            (username, hash_password(password), email)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username
        FROM users
        WHERE username = ? AND password = ?
        """,
        (username, hash_password(password))
    )

    user = cursor.fetchone()
    conn.close()

    return user is not None


def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, email
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            "username": user[0],
            "email": user[1] or ""
        }

    return None


def update_profile(old_username, new_username, email):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET username = ?, email = ?
            WHERE username = ?
            """,
            (new_username, email, old_username)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def change_password(username, current_password, new_password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ? AND password = ?
        """,
        (username, hash_password(current_password))
    )

    user = cursor.fetchone()

    if not user:
        conn.close()
        return False

    cursor.execute(
        """
        UPDATE users
        SET password = ?
        WHERE username = ?
        """,
        (hash_password(new_password), username)
    )

    conn.commit()
    conn.close()

    return True


def delete_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE username = ?
        """,
        (username,)
    )

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()

    return deleted

