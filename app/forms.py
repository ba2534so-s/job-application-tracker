from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SubmitField, URLField, ValidationError, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, URL
from helpers.queries import get_user_by_username, get_user_by_email


class ContactForm(FlaskForm):
    name = StringField(label="Contact Name", validators=[DataRequired()])
class AddForm(FlaskForm):
    company = StringField(label="Company*", validators=[DataRequired()])
    position = StringField(label="Job Position*", validators=[DataRequired()])
    contract_type = SelectField("Contract Type*", choices=[], validators=[DataRequired()])
    location = StringField(label="Location*", validators=[DataRequired()])
    url = URLField(label="Application URL", validators=[Optional(), URL()])
    add_button = SubmitField(label="Add Job")

class EditForm(FlaskForm):
    company = StringField(label="Company", validators=[DataRequired()])
    position = StringField(label="Job Position", validators=[DataRequired()])
    contract_type = SelectField(label="Contract Type", choices=[], validators=[DataRequired()])
    location = StringField(label="Location", validators=[DataRequired()])
    url = URLField(label="Application URL", validators=[Optional(), URL()])
    status = SelectField(label="Status", choices=[], validators=[DataRequired()])
    save_button = SubmitField(label="Save Changes")


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = get_user_by_username(username_to_check.data)
        if user:
            raise ValidationError("Username already exists! Please try a different username")
    
    def validate_email(self, email_to_check):
        user = get_user_by_email(email_to_check.data)
        if user:
            raise ValidationError("Email already exists! Please try a different email")

    username = StringField(label="Username", validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit_button = SubmitField(label="Register")


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    login_button = SubmitField(label="Login")


class DeleteApplicationForm(FlaskForm):
    delete_button = SubmitField(label="Delete")