import sqlite3
import os
from datetime import datetime


# ==========================================================
# DATABASE PATH
# ==========================================================

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

DATABASE_DIR = os.path.join(
    BASE_PATH,
    "database"
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "insightcivic.db"
)


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def initialize_database():

    # Create database folder if it does not exist
    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()


    # ======================================================
    # USERS TABLE
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT NOT NULL UNIQUE,

            email TEXT NOT NULL UNIQUE,

            password_hash TEXT NOT NULL,

            role TEXT NOT NULL DEFAULT 'user',

            created_at TEXT NOT NULL,

            last_login TEXT

        )
    """)


    # ======================================================
    # ANALYSIS HISTORY TABLE
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            analysis_date TEXT NOT NULL,

            analysis_hour INTEGER NOT NULL,

            crime_count REAL,

            crash_count REAL,

            rainfall REAL,

            temperature REAL,

            peak_hour INTEGER,

            risk_level TEXT,

            confidence REAL,

            top_factor TEXT,

            created_at TEXT NOT NULL,

            FOREIGN KEY (user_id)
                REFERENCES users(id)

        )
    """)


    connection.commit()

    connection.close()


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================================
# CREATE USER
# ==========================================================

def create_user(
    username,
    email,
    password_hash,
    role="user"
):

    connection = get_connection()

    cursor = connection.cursor()

    created_at = datetime.now().isoformat()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password_hash,
                role,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                username,
                email,
                password_hash,
                role,
                created_at
            )
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()

# ==========================================================
# UPDATE USER ROLE
# ==========================================================

def update_user_role(username, role):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET role = ?
        WHERE username = ?
        """,
        (
            role,
            username
        )
    )

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated

# ==========================================================
# FIND USER
# ==========================================================

def get_user_by_username(username):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    connection.close()

    return user


# ==========================================================
# FIND USER BY EMAIL
# ==========================================================

def get_user_by_email(email):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    return user

def get_all_users():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            email,
            role,
            created_at,
            last_login
        FROM users
        ORDER BY created_at DESC
        """
    )

    users = cursor.fetchall()

    connection.close()

    # Convert sqlite3.Row objects into normal dictionaries
    return [dict(user) for user in users]

def get_user_statistics():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE role = 'admin'"
    )
    total_admins = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE role = 'user'"
    )
    total_regular_users = cursor.fetchone()[0]

    connection.close()

    return {
        "total_users": total_users,
        "total_admins": total_admins,
        "total_regular_users": total_regular_users
    }

# ==========================================================
# UPDATE LAST LOGIN
# ==========================================================

def update_last_login(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET last_login = ?
        WHERE id = ?
        """,
        (
            datetime.now().isoformat(),
            user_id
        )
    )

    connection.commit()

    connection.close()


# ==========================================================
# SAVE ANALYSIS
# ==========================================================

def save_analysis(
    user_id,
    analysis_date,
    analysis_hour,
    crime_count,
    crash_count,
    rainfall,
    temperature,
    peak_hour,
    risk_level,
    confidence,
    top_factor
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO analysis_history
        (
            user_id,
            analysis_date,
            analysis_hour,
            crime_count,
            crash_count,
            rainfall,
            temperature,
            peak_hour,
            risk_level,
            confidence,
            top_factor,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            str(analysis_date),
            int(analysis_hour),
            float(crime_count),
            float(crash_count),
            float(rainfall),
            float(temperature),
            int(peak_hour),
            str(risk_level),
            float(confidence),
            str(top_factor),
            datetime.now().isoformat()
        )
    )

    connection.commit()

    connection.close()


# ==========================================================
# GET USER ANALYSIS HISTORY
# ==========================================================

def get_user_history(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM analysis_history
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    history = cursor.fetchall()

    connection.close()

    # Convert sqlite3.Row objects into normal dictionaries
    return [dict(record) for record in history]

