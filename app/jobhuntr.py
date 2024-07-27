from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint("jobhuntr", __name__)

@bp.route("/")
def index():
    print("Index route called")  # Debug print statement
    # Later we will present statistics and some type of dashboard/overview of the users applications
    return render_template("jobhuntr/index.html")

@bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        pass
    else:
        return render_template("jobhuntr/add.html")