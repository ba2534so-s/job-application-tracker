from functools import wraps
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db
from helpers.queries import create_user, get_user_by_username, get_user_by_id
from app.forms import RegisterForm, LoginForm

bp = Blueprint("auth",__name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        create_user(username=form.username.data,
                    email=form.email.data,
                    hashed_password=generate_password_hash(form.password.data))
        return redirect(url_for("auth.login"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error creating the user: {err_msg}", category="danger")

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user and check_password_hash(user["hashed_password"], form.password.data):
            session.clear()
            session["user_id"] = user["id"]
            flash(f"You are logged in as {user["username"]}", category="success")
            return redirect(url_for("index"))
        else: 
            flash("Wrong username or password! Please try again.", category="danger")

    return render_template("auth/login.html", form=form)
    '''
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
    '''

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(user_id)


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
