from flask import Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
from werkzeug.exceptions import abort
from app.auth import login_required
from helpers.queries import *
from app.forms import AddForm, DeleteApplicationForm

bp = Blueprint("jobhuntr", __name__)

@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    delete_form = DeleteApplicationForm()

    applications = get_all_applications_for_user(g.user["id"])
    contract_types = get_contract_types_dict()
    statuses = get_statuses_dict()
    
    return render_template("jobhuntr/index.html", 
                           applications=applications, 
                           contract_types=contract_types,
                           statuses=statuses,
                           delete_form=delete_form)

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    '''
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
            if check_existing_application(g.user["id"], company, position, contract_type, location, url, date_added):
                flash("You have already added this job recently")
                return redirect(url_for("jobhuntr.add"))
            
            add_job(g.user["id"], company, position, location, contract_type, url, date_added)
            flash("Job application added successfully.")
            return redirect(url_for("index"))



        # check radio button if user wants to add contact information
        # If yes, get contact info


    else:
        form = AddForm()
        form.contract_type.choices = [("", "Select Contract Type")] + get_contract_types_tuple()
        return render_template("jobhuntr/add.html", form=form)
    '''
        
    form = AddForm()
    form.contract_type.choices = [("", "Select Contract Type")] + get_contract_types_tuple()

    if form.validate_on_submit():
        url = form.url.data or None # If the URL is empty, store None
        add_job(user_id=g.user["id"],
                company=form.company.data,
                position=form.position.data,
                contract_type=form.contract_type.data,
                location=form.location.data,
                url=url)
        return redirect(url_for("index"))
    
    if form.errors != {}: # If there are errors from validations (errors returnes as dict)
        for err_msg in form.errors.values():
            flash(f"There was an error adding the job: {err_msg}", category="danger")

    return render_template("jobhuntr/add.html", form=form)

@bp.route("/delete", methods=["POST"])
def delete():
    form = DeleteApplicationForm()
    
    if form.validate_on_submit():

        job_id = request.form.get('job_id')
        if job_id is None:
            flash("Invalid job deletion request.", category="danger")
            return redirect(url_for("index"))
        
        job_to_delete = delete_job(g.user["id"], job_id)

        if job_to_delete:
            flash(f"Job '{job_to_delete['job_position']}' at '{job_to_delete['company_name']}' was deleted successfully.",
                category="warning")
        else:
            flash("Job could not be found or you don't have permission to delete it.", category="danger")
    else:
        flash("There was an error processing your request.", category="danger")
    
    return redirect(url_for("index"))
