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
    