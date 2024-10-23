from flask import Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
from werkzeug.exceptions import abort
from helpers.utils import *
from helpers.queries import *
from app.forms import AddForm, DeleteApplicationForm, EditForm

bp = Blueprint("jobhuntr", __name__)



@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    delete_form = DeleteApplicationForm()

    applications = get_all_applications_for_user(g.user["id"])
    contract_types = get_contract_types_dict()
    statuses = get_statuses_dict()
    contacts = get_all_contacts_for_user(g.user["id"])

    contacts_dict = {contact["id"] : contact for contact in contacts}
    
    return render_template("jobhuntr/index.html", 
                           applications=applications, 
                           contract_types=contract_types,
                           statuses=statuses,
                           contacts=contacts_dict,
                           delete_form=delete_form)



@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddForm()
    form.contract_type.choices = [("", "Select Contract Type")] + get_contract_types_tuple()

    if form.validate_on_submit():
        url = form.url.data or None # If the URL is empty, store None
        
        contact_info = None
        if form.contact.form.name.data:
            contact_info = {
                "name" : form.contact.form.name.data,
                "email" : form.contact.form.email.data or None,
                "phone" : form.contact.form.phone.data or None
            }
        
        add_job(user_id=g.user["id"],
                company=form.company.data,
                position=form.position.data,
                contract_type=form.contract_type.data,
                location=form.location.data,
                url=url,
                contact_info=contact_info)
        flash("Job added successfully", category="success")
        return redirect(url_for("index"))
    
    if form.errors != {}: # If there are errors from validations (errors returned as dict)
        for err_msg in form.errors.values():
            flash(f"There was an error adding the job: {err_msg}", category="danger")

    return render_template("jobhuntr/add.html", form=form)



@bp.route("/update-status/<int:job_id>/<int:status_id>")
@login_required
def update_status(job_id, status_id):
    job = get_job_by_id(g.user["id"], job_id)
    if job is None:
        flash("Something went wrong!Job was not found.", category="Danger")
        return redirect(url_for("index"))
    update_job_status(g.user["id"], job_id, status_id)
    return redirect(request.referrer or url_for("index"))


@bp.route("/edit/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit(job_id):
    job = get_job_by_id(g.user["id"], job_id)
    contact = get_contact_by_id(job["contact_id"]) if job["contact_id"] else None
    
    if job is None:
        flash("Job not found.", category="danger")
        return redirect(url_for("index"))

    form = EditForm()
    form.contract_type.choices = get_contract_types_tuple()
    form.status.choices = get_statuses_tuple()

    
    if form.validate_on_submit():
        # Handle job update
        update_job(g.user["id"], job_id, form.company.data, form.position.data, 
                   form.location.data, form.contract_type.data, form.url.data, form.status.data)
        
        # Handle contact or update or creation based on form data
        if form.contact.form.name.data:
            if contact and (form.contact.form.name.data != contact["contact_name"] or
                    form.contact.form.email.data != contact["email"] or
                    form.contact.form.phone.data != contact["phone_number"]):
                # Update contact if contact exists and one of the fields has been changed
                update_contact(contact["id"], 
                               form.contact.form.name.data,
                               form.contact.form.email.data,
                               form.contact.form.phone.data)
            else: 
                # Create new contact if there is no contact already
                contact_id = add_contact(
                    g.user["id"],
                    form.contact.form.name.data,
                    form.contact.form.email.data,
                    form.contact.form.phone.data
                )
                update_job_contact(job_id, contact_id)
        elif contact:
            # Remove contact if name field is empty
            delete_contact(contact["id"])
            update_job_contact(job_id, None)

        flash("Job updated successfully", category="success")
        return redirect(url_for("index"))
    
    # create populate_edit_form function to refactor this function
    form.company.data = job["company_name"]
    form.position.data = job["job_position"]
    form.contract_type.data = job["contract_type_id"]
    form.location.data = job["job_location"]
    form.status.data = job["status_id"]
    form.url.data = job["job_post_link"]
    if contact:
        form.contact.form.name.data = contact["contact_name"]
        form.contact.form.email.data = contact["email"]
        form.contact.form.phone.data = contact["phone_number"]

    return render_template("jobhuntr/edit.html", form=form, job=job, contact=contact)



@bp.route("/delete", methods=["POST"])
@login_required
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
