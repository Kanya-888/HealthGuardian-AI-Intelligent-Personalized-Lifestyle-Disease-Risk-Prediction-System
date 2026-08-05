import sqlite3

DATABASE = "database/healthguardian.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        age INTEGER,

        bmi REAL,

        health_score REAL,

        diabetes_risk REAL,

        calories REAL,

        water REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    conn.close()