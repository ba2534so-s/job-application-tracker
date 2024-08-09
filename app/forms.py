from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SubmitField, URLField
from wtforms.validators import Email, EqualTo, Length


class AddForm(FlaskForm):
    company = StringField(label="Company", validators=[])
    position = StringField(label="Job Position", validators=[])
    contract_type = SelectField("Contract Type", choices=[], validators=[])
    location = StringField(label="Location", validators=[])
    url = URLField(label="URL", validators=[])
    add_button = SubmitField(label="Add Job", validators=[])

class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[Length(min=3, max=30)])
    email = StringField(label="Email", validators=[Email()])
    password = PasswordField(label="Password", validators=[Length(min=8)])
    password_confirm = PasswordField(label="Confirm Password", validators=[EqualTo("password")])
    submit_button = SubmitField(label="Create User")
