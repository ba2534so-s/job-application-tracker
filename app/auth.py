from functools import wraps
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db
from helpers.queries import create_user, get_user_by_username

bp = Blueprint("auth",__name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        error = None

        if not username:
            error = "Username is required"
        elif not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"
        elif password != confirmation:
            error = "Confirmation is required"

        db = get_db()

        if error is None:
            success, error_message = create_user(username, email, password)
            if success:
                return redirect(url_for("auth.login")) 
            else:
                error = error_message
            
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
            user = get_user_by_username(username)
        
        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["hashed_password"], password):
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
        g.user = get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
