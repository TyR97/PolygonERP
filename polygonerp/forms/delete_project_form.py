from flask_wtf import FlaskForm
from wtforms.fields.simple import BooleanField, SubmitField

class DeleteProjectForm(FlaskForm):
    submit = SubmitField('Yes')