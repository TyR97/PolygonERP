from flask import render_template, request, redirect, url_for, flash, g, Blueprint
from datetime import date, datetime

from polygonerp.forms.delete_user_form import DeleteUserForm
from polygonerp.models.time_log import TimeLog
from polygonerp.models.user import User
from polygonerp.db import db
from polygonerp.models.project import Project
from polygonerp.forms.user_form import UserForm
from polygonerp.utils.email_utils import send_employee_termination_notification
from polygonerp.utils.decorators_util import login_required, admin_required
from polygonerp.utils.date_utils import  get_dates_for_current_month

class UserController():

    def __init__(self, blueprint, app):
        self.bp = blueprint
        self.bp.add_url_rule('/search', view_func=self.search_users, methods=['GET', 'POST'])
        self.bp.add_url_rule('/employee_dash', view_func=self.employee_dash, methods=['GET', 'POST'])
        self.bp.add_url_rule('/delete/<user_id>', view_func=admin_required(self.delete_user), methods=['GET', 'POST'])
        self.bp.add_url_rule('/edit_worker/<user_id>', view_func= admin_required(self.update_user), methods=['GET', 'POST'])

    def employee_dash(self):

        return render_template('user/employee_dash.html')

    def search_users(self):
        name_query = request.args.get('name', '').strip()
        email_query = request.args.get('email', '').strip()
        job_title_query = request.args.get('job_title', '').strip()

        filters = []
        if name_query:
            filters.append(User.name.ilike(f"%{name_query}%"))
        if email_query:
            filters.append(User.username.ilike(f"%{email_query}%"))
        if job_title_query:
            filters.append(User.job_title.ilike(f"%{job_title_query}%"))

        users = User.query.filter(*filters).order_by(User.name.asc()).all()  if filters else User.query.order_by(User.name.asc()).all()
        return render_template("user/search_users.html", users=users)

    def delete_user(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        project = Project.query.filter_by(supervisor_id=user.id).first()
        form = DeleteUserForm()

        if user == g.user:
            flash("You can't delete your own account!", "danger")
            return redirect(url_for('user.search_users'))

        if form.validate_on_submit():
            if form.terminated.data == 'yes':
                db.session.delete(user)
                db.session.delete(project)
                db.session.commit()
                send_employee_termination_notification(user)
                flash("User has been deleted!", "success")
                return redirect(url_for('user.search_users'))
            else:
                db.session.delete(user)
                db.session.delete(project)
                db.session.commit()
                flash("User has been deleted!", "success")
                return redirect(url_for('user.search_users'))


        return render_template("user/delete_user.html", user=user, form=form)


    def update_user(self, user_id):
        user = User.query.get_or_404(user_id)
        form = UserForm(obj=user)

        if form.validate_on_submit():
            form.populate_obj(user)
            db.session.commit()
            print('updated successfully')
            return redirect(url_for('user.search_users'))


        return render_template('user/update_user.html', user=user, form=form)

bp = Blueprint('user', __name__, url_prefix='/employee')

def init_user_controller(app):
    UserController(bp, app)
