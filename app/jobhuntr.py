from flask import Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db
from datetime import datetime

bp = Blueprint("jobhuntr", __name__)

@bp.route("/")
def index():
    print("Index route called")  # Debug print statement
    # Later we will present statistics and some type of dashboard/overview of the users applications
    return render_template("jobhuntr/index.html")

@bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        company = request.form.get("company")
        position = request.form.get("positon")
        contract_type = request.form.get("contract-type")
        location = request.form.get("location")
        url = request.form.get("url")
        force_submit = request.form.get("force-submit")
        date_added = datetime.now().isoformat(sep=" ", timespec="minutes")
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
            db = get_db()
            if force_submit != "true":
                existing_application = db.execute(
                    """
                    SELECT *
                    FROM applications
                    WHERE user_id = ?
                    AND company_name = ?
                    AND job_position = ?
                    AND job_location = ?
                    AND contract_type_id = ?
                    AND (date('now') - date(?)) < 150
                    """,
                    (g.user["id"], company, position, location, contract_type)
                ).fetchone()

                if existing_application:
                    return jsonify({"duplicate": True})
            
            db.execute(
                """
                INSERT INTO applications (
                    user_id, company_name, job_position, job_location, contract_type_id, job_post_link, date_added, status_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    g.user["id"], company, position, location, contract_type, url, date_added, 1
                )
            )
            db.commit()
            flash("Job application added successfully.")
            return redirect(url_for("index"))



        
        
            




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