from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, URLField


class AddForm(FlaskForm):
    company = StringField(label="Company")
    position = StringField(label="Position")
    contract_type = SelectField("Contract Type")
    location = StringField(label="Location")
    url = URLField(label="URL")
    add_button = SubmitField(label="Add Job")
