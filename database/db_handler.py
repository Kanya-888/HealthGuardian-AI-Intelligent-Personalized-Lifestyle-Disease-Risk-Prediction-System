"""
SQLite Database Handler for HealthGuardian AI
Provides schema initialization, parameterized CRUD operations, and security protection.
"""

import sqlite3
import json
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "healthguardian.db")


def get_connection() -> sqlite3.Connection:
    """Establish connection to SQLite database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables with schema definitions and auto-migration."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Check existing table columns for users
        cursor.execute("PRAGMA table_info(users);")
        user_cols = [col[1] for col in cursor.fetchall()]

        if user_cols and ("email" not in user_cols or "password_hash" not in user_cols):
            # Old schema detected, drop incompatible old tables to rebuild clean schema
            cursor.execute("DROP TABLE IF EXISTS predictions;")
            cursor.execute("DROP TABLE IF EXISTS patient_profiles;")
            cursor.execute("DROP TABLE IF EXISTS reminders;")
            cursor.execute("DROP TABLE IF EXISTS users;")
            conn.commit()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'patient',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Patient Profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                age INTEGER DEFAULT 30,
                gender TEXT DEFAULT 'Male',
                height REAL DEFAULT 170.0,
                weight REAL DEFAULT 70.0,
                blood_group TEXT DEFAULT 'O+',
                emergency_contact TEXT DEFAULT '',
                medical_history TEXT DEFAULT '',
                smoking TEXT DEFAULT 'Never',
                alcohol TEXT DEFAULT 'Never',
                sleep_hours REAL DEFAULT 7.5,
                stress_level TEXT DEFAULT 'Moderate',
                exercise_freq TEXT DEFAULT '3-4 days/week',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)

        # Predictions History table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                age INTEGER,
                bmi REAL,
                glucose REAL,
                blood_pressure REAL,
                diabetes_prob REAL,
                heart_prob REAL,
                hypertension_prob REAL,
                obesity_prob REAL,
                kidney_prob REAL,
                stroke_prob REAL,
                health_score INTEGER,
                details_json TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)

        # Reminders / Notifications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                reminder_type TEXT NOT NULL,
                frequency TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                is_enabled INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)

        conn.commit()


# --- User CRUD Operations ---

def create_user(username: str, email: str, password_hash: str, full_name: str, role: str = "patient") -> Tuple[bool, str]:
    """Create a new user in the database."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, full_name, role) VALUES (?, ?, ?, ?, ?)",
                (username.strip(), email.strip().lower(), password_hash, full_name.strip(), role)
            )
            user_id = cursor.lastrowid
            
            # Create default patient profile
            cursor.execute(
                "INSERT INTO patient_profiles (user_id) VALUES (?)",
                (user_id,)
            )
            conn.commit()
            return True, "User registered successfully!"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already exists."
        elif "email" in str(e):
            return False, "Email address already registered."
        return False, "User creation failed due to database conflict."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Retrieve user details by username using parameterized query."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username.strip(),))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve user by user ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_all_users() -> List[Dict[str, Any]]:
    """Retrieve list of all registered users (Admin utility)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, full_name, role, created_at FROM users ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


def update_user_password(user_id: int, new_password_hash: str) -> bool:
    """Update user password hash."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_password_hash, user_id))
        conn.commit()
        return cursor.rowcount > 0


def delete_user(user_id: int) -> bool:
    """Delete user and all associated records."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0


# --- Patient Profile CRUD ---

def get_patient_profile(user_id: int) -> Dict[str, Any]:
    """Get patient profile for a user ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient_profiles WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        else:
            # Create if missing
            cursor.execute("INSERT INTO patient_profiles (user_id) VALUES (?)", (user_id,))
            conn.commit()
            cursor.execute("SELECT * FROM patient_profiles WHERE user_id = ?", (user_id,))
            return dict(cursor.fetchone())


def update_patient_profile(user_id: int, profile_data: Dict[str, Any]) -> bool:
    """Update patient profile fields."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE patient_profiles SET
                age = ?, gender = ?, height = ?, weight = ?, blood_group = ?,
                emergency_contact = ?, medical_history = ?, smoking = ?, alcohol = ?,
                sleep_hours = ?, stress_level = ?, exercise_freq = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (
            profile_data.get("age", 30),
            profile_data.get("gender", "Male"),
            profile_data.get("height", 170.0),
            profile_data.get("weight", 70.0),
            profile_data.get("blood_group", "O+"),
            profile_data.get("emergency_contact", ""),
            profile_data.get("medical_history", ""),
            profile_data.get("smoking", "Never"),
            profile_data.get("alcohol", "Never"),
            profile_data.get("sleep_hours", 7.5),
            profile_data.get("stress_level", "Moderate"),
            profile_data.get("exercise_freq", "3-4 days/week"),
            user_id
        ))
        conn.commit()
        return cursor.rowcount > 0


# --- Prediction History CRUD ---

def save_prediction(user_id: int, age: int, bmi: float, glucose: float, blood_pressure: float,
                    diabetes_prob: float, heart_prob: float, hypertension_prob: float,
                    obesity_prob: float, kidney_prob: float, stroke_prob: float,
                    health_score: int, details: dict) -> int:
    """Save a disease risk assessment log to predictions table."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predictions (
                user_id, age, bmi, glucose, blood_pressure,
                diabetes_prob, heart_prob, hypertension_prob, obesity_prob, kidney_prob, stroke_prob,
                health_score, details_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, age, bmi, glucose, blood_pressure,
            diabetes_prob, heart_prob, hypertension_prob, obesity_prob, kidney_prob, stroke_prob,
            health_score, json.dumps(details)
        ))
        conn.commit()
        return cursor.lastrowid


def get_user_predictions(user_id: int) -> List[Dict[str, Any]]:
    """Retrieve prediction history for a given user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM predictions WHERE user_id = ? ORDER BY timestamp DESC
        """, (user_id,))
        rows = cursor.fetchall()
        result = []
        for r in rows:
            item = dict(r)
            if item.get("details_json"):
                try:
                    item["details"] = json.loads(item["details_json"])
                except Exception:
                    item["details"] = {}
            result.append(item)
        return result


def get_all_predictions() -> List[Dict[str, Any]]:
    """Retrieve all predictions for admin overview."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, u.username, u.full_name FROM predictions p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.timestamp DESC
        """)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


def delete_prediction(prediction_id: int, user_id: Optional[int] = None) -> bool:
    """Delete a prediction record."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("DELETE FROM predictions WHERE id = ? AND user_id = ?", (prediction_id, user_id))
        else:
            cursor.execute("DELETE FROM predictions WHERE id = ?", (prediction_id,))
        conn.commit()
        return cursor.rowcount > 0


# Initialize DB automatically on module import
init_db()
