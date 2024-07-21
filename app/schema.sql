DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS applications;


CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL
);

CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    company_name TEXT NOT NULL,
    job_position TEXT NOT NULL,
    job_location TEXT,
    contract_type_id INTEGER,
    contact_id INTEGER,
    job_post_link TEXT,
    date_added DATE NOT NULL,
    date_applied DATE,
    status_id INTEGER NOT NULL,
    job_description TEXT,
    cover_letter TEXT,
    FOREIGN KEY (user_id) references users (id),
    FOREIGN KEY (contract_type_id) references contract_types (id),
    FOREIGN KEY (contact_id) references contacts (id),
    FOREIGN KEY (status_id) references statuses (id)
);