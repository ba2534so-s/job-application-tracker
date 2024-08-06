from flask import Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db
from datetime import datetime
from helpers.queries import *

bp = Blueprint("jobhuntr", __name__)

@bp.route("/")
@login_required
def index():
    applications = get_all_applications_for_user(g.user["id"])
    contract_types = get_contract_types_dict()
    statuses = get_statuses_dict()
    
    return render_template("jobhuntr/index.html", 
                           applications=applications, 
                           contract_types=contract_types,
                           statuses=statuses)

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        company = request.form.get("company")
        position = request.form.get("position")
        contract_type = request.form.get("contract-type")
        location = request.form.get("location")
        url = request.form.get("url")
        date_added = datetime.now().strftime("%Y-%m-%d")
        error = None

        if not company:
            error = "Company name required"
        elif not position:
            error = "Position required"
        elif not contract_type:
            error = "Contract type required"
        elif not location:
            error = "Location required"
        
        if error is None:
            try:
                if check_existing_application(g.user["id"], company, position, contract_type, location, url, date_added):
                    flash("You have already added this job recently")
                    return redirect(url_for("jobhuntr.add"))
                
                add_job(g.user["id"], company, position, location, contract_type, url, date_added)
                flash("Job application added successfully.")
                return redirect(url_for("index"))
            except db.IntegrityError:
                flash("An error occurred while adding the job application. Please try again.")
                return redirect(url_for("jobhuntr.add"))


        # check radio button if user wants to add contact information
        # If yes, get contact info


    else:
        # Fill the contract type select
        db = get_db()
        try:
            contract_types = db.execute("SELECT * FROM contract_types").fetchall()
        except:
            pass
        
        return render_template("jobhuntr/add.html", contract_types=contract_types)