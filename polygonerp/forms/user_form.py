from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Name is required")])
    maiden_name = StringField('Maiden Name')
    mothers_name = StringField('Mothers Name', validators=[DataRequired(message="Mother's name is required")])
    pob = StringField('Place of Birth', validators=[DataRequired(message="Place of Birth is required")])
    dob = StringField('Date of Birth', validators=[DataRequired(message="Date of Birth is required")])
    address = StringField('Address', validators=[DataRequired(message="Address is required")])
    tax_num = StringField('Tax Number', validators=[DataRequired(message="Tax number required")])
    taj_number = StringField('Taj Number', validators=[DataRequired(message="Taj number is required")])
    job_title = StringField('Job Title', validators=[DataRequired(message="Job title is required")])
    base_pay = IntegerField('Base Pay', validators=[DataRequired(message="Base pay is required"), NumberRange(min=1, message="Must be a positive number.")])


