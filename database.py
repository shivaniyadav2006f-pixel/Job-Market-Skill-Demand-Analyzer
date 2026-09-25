import sqlite3
import hashlib
from datetime import datetime

DB_NAME = "users.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return sqlite3.connect(DB_NAME)


# =========================================================
# CREATE TABLES
# =========================================================

def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------------------------------
    # USERS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT DEFAULT '',
            role TEXT DEFAULT 'user'
        )
    """)

    # -----------------------------------------------------
    # OLD DATABASE COMPATIBILITY
    # -----------------------------------------------------

    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]

    if "email" not in columns:

        cursor.execute(
            "ALTER TABLE users ADD COLUMN email TEXT DEFAULT ''"
        )

    if "role" not in columns:

        cursor.execute(
            "ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'"
        )

    # -----------------------------------------------------
    # LOGIN HISTORY TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            login_time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# PASSWORD HASH
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================================================
# REGISTER USER
# =========================================================

def register_user(
    username,
    password,
    email=""
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username, password, email, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                hash_password(password),
                email,
                "user"
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# =========================================================
# LOGIN USER
# =========================================================

def login_user(
    username,
    password
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    # -----------------------------------------------------
    # SAVE LOGIN HISTORY
    # -----------------------------------------------------

    if user:

        login_time = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        cursor.execute(
            """
            INSERT INTO login_history
            (username, login_time)
            VALUES (?, ?)
            """,
            (
                username,
                login_time
            )
        )

        conn.commit()

    conn.close()

    return user is not None


# =========================================================
# GET USER
# =========================================================

def get_user(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, email, role
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
            "email": user[1] or "",
            "role": user[2] or "user"
        }

    return None


# =========================================================
# UPDATE PROFILE
# =========================================================

def update_profile(
    old_username,
    new_username,
    email
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            UPDATE users
            SET username = ?, email = ?
            WHERE username = ?
            """,
            (
                new_username,
                email,
                old_username
            )
        )

        # Keep login history connected to renamed username
        cursor.execute(
            """
            UPDATE login_history
            SET username = ?
            WHERE username = ?
            """,
            (
                new_username,
                old_username
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# =========================================================
# CHANGE PASSWORD
# =========================================================

def change_password(
    username,
    current_password,
    new_password
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (
            username,
            hash_password(current_password)
        )
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
        (
            hash_password(new_password),
            username
        )
    )

    conn.commit()
    conn.close()

    return True


# =========================================================
# DELETE USER
# =========================================================

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

    deleted = cursor.rowcount > 0

    # Remove login history also
    cursor.execute(
        """
        DELETE FROM login_history
        WHERE username = ?
        """,
        (username,)
    )

    conn.commit()
    conn.close()

    return deleted


# =========================================================
# ADMIN CHECK
# =========================================================

def is_admin(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    return (
        result is not None
        and result[0] == "admin"
    )


# =========================================================
# CREATE ADMIN ACCOUNT
# =========================================================

def create_admin_account(
    username,
    password,
    email=""
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    existing = cursor.fetchone()

    if existing:

        cursor.execute(
            """
            UPDATE users
            SET role = 'admin'
            WHERE username = ?
            """,
            (username,)
        )

    else:

        cursor.execute(
            """
            INSERT INTO users
            (username, password, email, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                hash_password(password),
                email,
                "admin"
            )
        )

    conn.commit()
    conn.close()


# =========================================================
# GET ALL USERS
# =========================================================

def get_all_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            email,
            role
        FROM users
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# =========================================================
# SEARCH USERS
# =========================================================

def search_users(search_text=""):

    conn = get_connection()
    cursor = conn.cursor()

    search_text = search_text.strip()

    if search_text:

        cursor.execute(
            """
            SELECT
                id,
                username,
                email,
                role
            FROM users
            WHERE username LIKE ?
            OR email LIKE ?
            ORDER BY id DESC
            """,
            (
                f"%{search_text}%",
                f"%{search_text}%"
            )
        )

    else:

        cursor.execute(
            """
            SELECT
                id,
                username,
                email,
                role
            FROM users
            ORDER BY id DESC
            """
        )

    rows = cursor.fetchall()

    conn.close()

    return rows


# =========================================================
# TOTAL USERS
# =========================================================

def get_user_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE role != 'admin'
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


# =========================================================
# GET LOGIN HISTORY
# =========================================================

def get_login_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            username,
            login_time
        FROM login_history
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# =========================================================
# CLEAR LOGIN HISTORY
# =========================================================

def clear_login_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM login_history"
    )

    conn.commit()
    conn.close()


# =========================================================
# DELETE USER LOGIN HISTORY
# =========================================================

def clear_user_data(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM login_history
        WHERE username = ?
        """,
        (username,)
    )

    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted


# =========================================================
# INITIALIZE DATABASE
# =========================================================

create_table()

# =========================================================
# RESUME STORAGE TABLE
# =========================================================

def create_resume_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            stored_filename TEXT NOT NULL,
            upload_time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# ACTIVITY LOG TABLE
# =========================================================

def create_activity_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            activity TEXT NOT NULL,
            activity_time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# SAVE RESUME DETAILS
# =========================================================

def save_resume_record(
    username,
    original_filename,
    stored_filename
):

    conn = get_connection()
    cursor = conn.cursor()

    upload_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO resumes
        (
            username,
            original_filename,
            stored_filename,
            upload_time
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            original_filename,
            stored_filename,
            upload_time
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# GET ALL RESUMES
# =========================================================

def get_all_resumes():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            original_filename,
            stored_filename,
            upload_time
        FROM resumes
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# =========================================================
# GET USER RESUMES
# =========================================================

def get_user_resumes(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            original_filename,
            stored_filename,
            upload_time
        FROM resumes
        WHERE username = ?
        ORDER BY id DESC
        """,
        (username,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# =========================================================
# DELETE RESUME RECORD
# =========================================================

def delete_resume_record(resume_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM resumes
        WHERE id = ?
        """,
        (resume_id,)
    )

    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted


# =========================================================
# SAVE ACTIVITY LOG
# =========================================================

def log_activity(username, activity):

    conn = get_connection()
    cursor = conn.cursor()

    activity_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO activity_log
        (
            username,
            activity,
            activity_time
        )
        VALUES (?, ?, ?)
        """,
        (
            username,
            activity,
            activity_time
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# GET ALL ACTIVITY LOGS
# =========================================================

def get_activity_logs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            username,
            activity,
            activity_time
        FROM activity_log
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# =========================================================
# INITIALIZE NEW TABLES
# =========================================================

create_resume_table()
create_activity_table()