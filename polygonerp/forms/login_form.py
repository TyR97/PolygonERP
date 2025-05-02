"""
    Represents a login form for user authentication.
"""
from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
