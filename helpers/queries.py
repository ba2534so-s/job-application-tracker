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
def get_contract_types_dict():
    db = get_db()
    contract_types = db.execute("SELECT * FROM contract_types").fetchall()

    contract_types_dict = {} 
    for contract_type in contract_types:
        contract_types_dict[contract_type["id"]] = contract_type["contract_type"]

    return contract_types_dict

# APPLICATION STATUSES
def get_statuses_dict():
    db = get_db()
    statuses = db.execute("SELECT * FROM statuses").fetchall()

    statuses_dict = {}
    for status in statuses:
        statuses_dict[status["id"]] = status["application_status"]
    return statuses_dict

# APPLICATIONS
# add job
# get all added jobs for a user
def get_all_applications_for_user(user_id):
    db = get_db()
    applications = db.execute("SELECT * FROM applications WHERE user_id = ?", (user_id,)).fetchall()
    return applications

# get all jobs with status not started
# get all jobs with status applied
# get all jobs with status interviewing
# apply to job
# edit job application
# remove job 