from flask import Blueprint, flash, g, redirect, render_template, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from helpers.queries import create_user, get_user_by_username, get_user_by_id
from app.forms import RegisterForm, LoginForm

bp = Blueprint("auth",__name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = create_user(username=form.username.data,
                    email=form.email.data,
                    hashed_password=generate_password_hash(form.password.data))        
        session.clear()
        session["user_id"] = user_id
        flash("Registration successful! You are now logged in")
        return redirect(url_for("index"))
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
            flash(f"You are logged in as {user['username']}", category="success")
            return redirect(url_for("index"))
        else: 
            flash("Wrong username or password! Please try again.", category="danger")

    return render_template("auth/login.html", form=form)
   

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
    flash("You have been logged out", category="info")
    return redirect(url_for("index"))

