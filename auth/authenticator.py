"""
Authentication Module for HealthGuardian AI
Handles password hashing (bcrypt), authentication, session state management, and user registration.
"""

import bcrypt
import streamlit as st
from typing import Optional, Dict, Any, Tuple
from database.db_handler import (
    create_user, get_user_by_username, get_user_by_id,
    update_user_password, get_patient_profile
)


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify raw password against bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False


def init_session_state():
    """Ensure all required session state variables exist."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "patient_profile" not in st.session_state:
        st.session_state.patient_profile = None
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    if "page" not in st.session_state:
        st.session_state.page = "Home"


def login(username_or_email: str, password: str) -> Tuple[bool, str]:
    """Attempt user authentication."""
    if not username_or_email or not password:
        return False, "Please enter both username and password."

    user = get_user_by_username(username_or_email)
    if not user:
        return False, "Invalid username or password."

    if verify_password(password, user["password_hash"]):
        st.session_state.authenticated = True
        st.session_state.user = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"]
        }
        st.session_state.patient_profile = get_patient_profile(user["id"])
        return True, f"Welcome back, {user['full_name']}!"
    else:
        return False, "Invalid username or password."


def register(username: str, email: str, password: str, confirm_password: str, full_name: str, role: str = "patient") -> Tuple[bool, str]:
    """Register a new user account."""
    if not username or not email or not password or not full_name:
        return False, "All fields are required."

    if len(username) < 3:
        return False, "Username must be at least 3 characters long."

    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address."

    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    if password != confirm_password:
        return False, "Passwords do not match."

    pwd_hash = hash_password(password)
    success, msg = create_user(username, email, pwd_hash, full_name, role)
    return success, msg


def logout():
    """Clear active user session."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.patient_profile = None
    st.session_state.page = "Login"


def reset_password(username: str, email: str, new_password: str) -> Tuple[bool, str]:
    """Reset password for a user with matching email."""
    user = get_user_by_username(username)
    if not user:
        return False, "Username not found."
    if user["email"].lower() != email.strip().lower():
        return False, "Email does not match our records."
    
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters long."

    new_hash = hash_password(new_password)
    if update_user_password(user["id"], new_hash):
        return True, "Password reset successfully. You can now login with your new password."
    return False, "Failed to update password. Please try again."


def is_admin() -> bool:
    """Check if current logged in user has admin privileges."""
    return (
        st.session_state.get("authenticated", False)
        and st.session_state.get("user")
        and st.session_state.user.get("role") == "admin"
    )
