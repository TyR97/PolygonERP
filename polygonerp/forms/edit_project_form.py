from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired
from polygonerp.models.user import User

class UpdateProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    finish_date = DateField('Finish Date', format='%Y-%m-%d', validators=[DataRequired()])
    supervisor_id = SelectField('Supervisor', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Project')

    def populate_supervisor_choices(self):
        self.supervisor_id.choices = [
            (user.id, user.name) for user in User.query.order_by(User.name).all()
        ]
