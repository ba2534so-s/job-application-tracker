import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint("auth",__name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif password != confirmation:
            error = "Confirmation is required"

        db = get_db()

        if error is None:
            try:
                db.execute(
                    # the arguments for the query might have to be within ()
                    "INSERT INTO user (username, hashed_password) VALUES (? , ?)", (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login")) 
            
        
        flash(error)
    
    else:
        return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"

        if error is None:
            db = get_db()
            # the argument for the query might have to be within ()
            user = db.execute("SELECT * FROM users WHERE username = ?", (username)).fetchone()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"
        
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        
        flash(error)

    else:
        return render_template("auth/login.html")
    
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db.execute("SELECT * FROM users WHERE id = ?", (user_id)).fetchone()
     