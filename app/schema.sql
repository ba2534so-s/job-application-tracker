DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS statuses;
DROP TABLE IF EXISTS contract_types;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS skills;


CREATE TABLE users (
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

CREATE TABLE statuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_status TEXT UNIQUE NOT NULL
);

CREATE TABLE contract_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_type TEXT UNIQUE NOT NULL 
);

CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT,
    email TEXT,
    phone_number TEXT
);

CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill TEXT UNIQUE NOT NUll 
);

CREATE TABLE application_skills (
    application_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    FOREIGN KEY (application_id) references applications (id),
    FOREIGN KEY (skill_id) references skills (id),
    PRIMARY KEY (application_id, skill_id)
);


INSERT INTO statuses (application_status) VALUES
('Not Started'),
('Applied'),
('Interviewing'),
('Rejected'),
('Job Offer'),
('Expired');

INSERT INTO contract_types (contract_type) VALUES
('Full-Time'),
('Part-Time'),
('Contract'),
('Temporary'),
('Internship'),
('Freelance'),
('Student Job');