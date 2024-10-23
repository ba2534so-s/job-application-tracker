from functools import wraps
from flask import g, redirect, url_for

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view



def populate_edit_form(form, job, contact):
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


def manage_contact(form, contact, job_id):
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