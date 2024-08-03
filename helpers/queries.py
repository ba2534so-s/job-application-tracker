from app.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash


# USERS
def create_user(username, email, password):
    db = get_db()
    db.execute("INSERT INTO users (id, email, hashed_password) VALUES (?, ?, ?)",
               (username, email, generate_password_hash(password)))
    db.commit()

