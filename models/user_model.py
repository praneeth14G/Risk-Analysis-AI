# models/user_model.py
# Defines user roles and sample login credentials

# In a real app you'd use a database. For a demo, a dictionary is fine.
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "name": "Admin User"
    },
    "officer1": {
        "password": "risk2024",
        "role": "user",
        "name": "Risk Officer"
    }
}

def get_user(username):
    """Return user dict if found, else None."""
    return USERS.get(username)

def verify_password(username, password):
    """Return True if username+password match."""
    user = get_user(username)
    if user and user["password"] == password:
        return True
    return False