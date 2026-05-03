# services/auth_service.py
# Handles login logic and session checks

from models.user_model import verify_password, get_user

def login_user(username, password):
    """
    Returns user dict if credentials are valid.
    Returns None if invalid.
    """
    if verify_password(username, password):
        return get_user(username)
    return None

def is_admin(session):
    """Check if the currently logged-in user is an admin."""
    return session.get("role") == "admin"

def is_logged_in(session):
    """Check if any user is logged in."""
    return "username" in session