from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo, Regexp, Length

"""
    Represents Forms for handling user password changes.
"""
class ChangePasswordForm(FlaskForm):
    password  = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password', message='Passwords must match'),
        Length(min=8, max=16, message="Password must be between 8 and 16 characters."),
        Regexp(r'^[A-Za-z0-9]+$', message="Password must be alphanumeric.")])
    submit = SubmitField('Change Password')
