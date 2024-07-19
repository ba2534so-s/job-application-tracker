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
        elif not confirmation:
            error = "Confirmation is required"

        db = get_db()

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, hashed_password) VALUES (? , ?)", username, generate_password_hash(password)
                )
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login")) 
            
        
        flash(error)
    
    else:
        return render_template("auth/register.html")

        