from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class ChangePasswordForm(FlaskForm):
    password  = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Change Password')
