import sqlite3
import click
from flask import current_app, g

# Later try to learn and use SQLAlchemy


# Creates (if not already created) and returns a database connection
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# Closes database connection if one exists
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()