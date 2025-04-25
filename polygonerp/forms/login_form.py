from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
