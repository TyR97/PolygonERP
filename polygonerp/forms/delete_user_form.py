from flask_wtf import FlaskForm
from wtforms.fields.simple import BooleanField, SubmitField


class DeleteUserForm(FlaskForm):
    terminated = BooleanField('Is the user\'s contract terminated?')
    submit = SubmitField('Yes')