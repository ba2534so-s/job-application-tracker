from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, URLField
from helpers.queries import get_contract_types_tuple


class AddForm(FlaskForm):
    company = StringField(label="Company")
    position = StringField(label="Position")
    contract_type = SelectField("Contract Type", choices=get_contract_types_tuple())
    location = StringField(label="Location")
    url = URLField(label="URL")
    add_button = SubmitField(label="Add Job")
