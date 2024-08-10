from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SubmitField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, URL


class AddForm(FlaskForm):
    company = StringField(label="Company", validators=[DataRequired()])
    position = StringField(label="Job Position", validators=[DataRequired()])
    contract_type = SelectField("Contract Type", choices=[], validators=[DataRequired()])
    location = StringField(label="Location", validators=[DataRequired()])
    url = URLField(label="URL", validators=[Optional(), URL()])
    add_button = SubmitField(label="Add Job")

class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit_button = SubmitField(label="Create User")
