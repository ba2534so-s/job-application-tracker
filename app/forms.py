from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SubmitField, URLField


class AddForm(FlaskForm):
    company = StringField(label="Company")
    position = StringField(label="Job Position")
    contract_type = SelectField("Contract Type", choices=[])
    location = StringField(label="Location")
    url = URLField(label="URL")
    add_button = SubmitField(label="Add Job")

class RegisterForm(FlaskForm):
    username = StringField(label="Username")
    email = StringField(label="Email")
    password = PasswordField(label="Password")
    password_confirm = PasswordField(label="Confirm Password")
    submit_button = SubmitField(label="Create User")
