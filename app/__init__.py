import os
from flask import Flask

def create_app(test_config=None):
    # Creates and configures app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",   # Needs to be changed when deploying
        DATABASE=os.path.join(app.instance_path, "app.sqlite")
    )

    if test_config is None:
        # Loads the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Loads the test config if it is passed in
        app.config.from_mapping(test_config)

    # Make sure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    return app