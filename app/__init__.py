import os
from flask import Flask
from flask_session import Session

def create_app(test_config=None):
    # Creates and configures app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",   # Needs to be changed when deploying
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
        SESSION_PERMANENT=False,
        SESSION_TYPE="filesystem",
        SESSION_FILE_DIR=os.path.join(app.instance_path, "flask_session")
    )
    
    # Initialize the session with the app
    Session(app)

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

    from . import auth
    app.register_blueprint(auth.bp)

    from . import app
    app.register_blueprint(app.bp)

    # Ensure responses aren't cached
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    return app