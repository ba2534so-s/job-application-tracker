from app.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash


# USERS
def create_user(username, email, password):
    db = get_db()
    try:
        db.execute("INSERT INTO users (id, email, hashed_password) VALUES (?, ?, ?)",
                   (username, email, generate_password_hash(password)))
        db.commit()
        return True, None
    except db.IntegrityError as e:
        error_message = f"User {username} or email {email} is already registered."
        return False, error_message
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        return False, error_message
    

def get_user_by_id(id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    return user

def get_user_by_username(username):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    return user



# CONTRACT TYPES

# APPLICATION STATUSES


# APPLICATIONS