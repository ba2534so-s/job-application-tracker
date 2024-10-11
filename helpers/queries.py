from app.db import get_db
from datetime import datetime, timedelta


# USERS
def create_user(username, email, hashed_password):
    db = get_db()

    cursor = db.execute("INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
                (username, email, hashed_password)
    )
    db.commit()
    return cursor.lastrowid

        
    

def get_user_by_id(id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    return user

def get_user_by_username(username):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    return user

def get_user_by_email(email):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    return user 


# CONTRACT TYPES
def get_contract_types():
    db = get_db()
    contract_types = db.execute("SELECT * FROM contract_types").fetchall()
    return contract_types


def get_contract_types_tuple():
    contract_types_tuple = []
    for contract_type in get_contract_types():
        contract_types_tuple.append((contract_type["id"], contract_type["contract_type"]))
    
    return contract_types_tuple

def get_contract_types_dict():
    contract_types_dict = {} 
    for contract_type in get_contract_types():
        contract_types_dict[contract_type["id"]] = contract_type["contract_type"]

    return contract_types_dict

# APPLICATION STATUSES
def get_statuses():
    db = get_db()
    statuses = db.execute("SELECT * FROM statuses").fetchall()
    return statuses


def get_statuses_tuple():
    statuses_tuple = []
    for status in get_statuses():
        statuses_tuple.append((status["id"], status["application_status"]))
    return statuses_tuple

def get_statuses_dict():
    db = get_db()
    statuses = db.execute("SELECT * FROM statuses").fetchall()

    statuses_dict = {}
    for status in statuses:
        statuses_dict[status["id"]] = status["application_status"]
    return statuses_dict

# APPLICATIONS
# add job
def add_job(user_id, company, position, location, contract_type, url, contact_info):
    date_added = datetime.now().strftime("%Y-%m-%d")
    db = get_db()
    
    contact_id = None
    if contact_info is not None:
        contact_id = add_contact(contact_info) if contact_info else None
    
    db.execute(
        """
        INSERT INTO applications (
            user_id, company_name, job_position, job_location, contract_type_id, job_post_link, date_added, status_id, contact_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id, company, position, location, contract_type, url, date_added, 1, contact_id
        )
    )
    db.commit()

def update_job_status(user_id, application_id, new_status):
    db = get_db()
    
    current_job = get_job_by_id(user_id, application_id)
    current_status_id = current_job["status_id"]

    if int(new_status) == 1:
        date_applied = None
        db.execute("UPDATE applications SET status_id = ?, date_applied = ? WHERE user_id = ? AND id = ?"
                   , (new_status, date_applied, user_id, application_id))
    elif current_status_id == 1:
        date_applied = datetime.now().strftime("%Y-%m-%d")
        db.execute("UPDATE applications SET status_id = ?, date_applied = ? WHERE user_id = ? AND id = ?"
                   , (new_status, date_applied, user_id, application_id))
    else:
        db.execute("UPDATE applications SET status_id = ? WHERE user_id = ? AND id = ?", 
                   (new_status, user_id, application_id))
    db.commit()

# edit job/application
def update_job(user_id, application_id, company, position, location, contract_type, url, status):
    db = get_db()
    
    current_job = get_job_by_id(user_id, application_id)
    current_status_id = current_job["status_id"]
    
    
    if int(status) == 1:
        date_applied = None
    elif current_status_id == 1:
        date_applied = datetime.now().strftime("%Y-%m-%d")
    else:
        date_applied = current_job["date_applied"]

    db.execute(
        '''
        UPDATE applications
        SET company_name = ?, job_position = ?, job_location = ?, 
            contract_type_id = ?, job_post_link = ?, date_applied = ?, status_id = ?
        WHERE user_id = ? AND id = ?
        ''',
        (company, position, location, contract_type, url, date_applied, status, user_id, application_id)
    )
    db.commit()

# check existing job
def check_existing_application(user_id, company, position, location, contract_type, url):
    date_threshold = (datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d")
    db = get_db()
    existing_application = db.execute(
        """
        SELECT *
        FROM applications
        WHERE user_id = ?
        AND company_name = ?
        AND job_position = ?
        AND job_location = ?
        AND contract_type_id = ?
        AND date_added >= ?
        """,
        (user_id, company, position, location, contract_type, url, date_threshold)
    ).fetchone()
    if existing_application:
        return True
    else:
        return False



# get all added jobs for a user
def get_all_applications_for_user(user_id):
    db = get_db()
    applications = db.execute("SELECT * FROM applications WHERE user_id = ?", (user_id,)).fetchall()
    return applications

def get_job_by_id(user_id, job_id):
    db = get_db()
    job = db.execute("SELECT * FROM applications WHERE user_id = ? AND id = ?", (user_id, job_id)).fetchone()
    return job

# get all jobs with status not started
# get all jobs with status applied
# get all jobs with status interviewing

# delete job 
def delete_job(user_id, job_id):
    db = get_db()
    job_to_delete = db.execute("SELECT * FROM applications WHERE user_id = ? AND id = ?", (user_id, job_id)).fetchone()

    if job_to_delete:
        db.execute("DELETE FROM applications WHERE user_id = ? AND id = ?", (user_id, job_id))
        db.commit()
        return job_to_delete
    return None

# Update the contact_id for a job when a new contact is added or an existing contact is removed.
def update_job_contact(job_id, contact_id):
    db = get_db()
    db.execute("UPDATE applications SET contact_id = ? WHERE id = ?", (contact_id, job_id))
    db.commit()


#CONTACTS
def add_contact(contact_info):
    db = get_db()
    
    cursor = db.execute(
        """
        INSERT INTO contacts (contact_name, email, phone_number)
        VALUES (?, ?, ?)""", 
        (contact_info["name"], contact_info["email"], contact_info["phone"]))
    db.commit()
    return cursor.lastrowid

def get_contact_by_id(id):
    db = get_db()
    contact = db.execute("SELECT * FROM contacts WHERE id = ?", (id,)).fetchone()
    return contact

# Update existing contacts information
def update_contact(contact_id, name, email, phone):
    db = get_db()
    db.execute("UPDATE contacts SET contact_name = ?, email = ?, phone_number = ? WHERE contact_id = ?", 
               (name, email, phone, contact_id)
    )
    db.commit()

def delete_contact(contact_id):
    db = get_db()
    db.execute("DELETE FROM contacts where id = ?", (contact_id,))
    db.commit()
