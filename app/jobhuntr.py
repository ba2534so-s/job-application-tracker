from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint("index", __name__)

bp.route("/")
def index():
    # Later we will present statistics and some type of dashboard/overview of the users applications
    return render_template("jobhuntr/index.html")