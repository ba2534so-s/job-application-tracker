from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SubmitField, URLField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, URL
from helpers.queries import get_user_by_username, get_user_by_email


class AddForm(FlaskForm):
    company = StringField(label="Company*", validators=[DataRequired()])
    position = StringField(label="Job Position*", validators=[DataRequired()])
    contract_type = SelectField("Contract Type*", choices=[], validators=[DataRequired()])
    location = StringField(label="Location*", validators=[DataRequired()])
    url = URLField(label="URL", validators=[Optional(), URL()])
    add_button = SubmitField(label="Add Job")

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
