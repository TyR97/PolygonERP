from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo

"""
    Represents Forms for handling user password changes.
"""
class ChangePasswordForm(FlaskForm):
    password  = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Change Password')

class ChangePasswordWithUsernameForm(ChangePasswordForm):
    username = StringField('Username', validators=[DataRequired()])