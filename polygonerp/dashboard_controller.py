from flask import render_template, request, redirect, url_for, flash, g
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, datetime

from polygonerp.forms.delete_user_form import DeleteUserForm
from polygonerp.models.time_log import TimeLog
from polygonerp.models.user import User
from polygonerp.db import db
from polygonerp.models.project import Project
from polygonerp.forms.user_form import UserForm
from polygonerp.utils.email_utils import send_employee_termination_notification
from polygonerp.utils.utils import login_required, admin_required
from polygonerp.utils.date_utils import  get_dates_for_current_month

#TODO separate projects to own controller
class DashboardController:
    def __init__(self, blueprint, app):
        self.bp = blueprint

        # Registering routes for Blueprint
        blueprint.add_url_rule('/', view_func=login_required(self.dashboard), methods=['GET', 'POST'])
        blueprint.add_url_rule('/profile/<user_id>', view_func=self.profile_view, methods=['GET', 'POST'])
        blueprint.add_url_rule('/search', view_func=self.search_users, methods=['GET', 'POST'])
        blueprint.add_url_rule('/delete/<user_id>', view_func=admin_required(self.delete_user), methods=['GET', 'POST'])
        blueprint.add_url_rule('/edit_worker/<user_id>', view_func= admin_required(self.update_user), methods=['GET', 'POST'])
        blueprint.add_url_rule('/projects/create', view_func=admin_required(self.create_project), methods=['GET', 'POST'])
        blueprint.add_url_rule('/log', view_func=self.time_log, methods=['GET', 'POST'])
        blueprint.add_url_rule('/projects', view_func=self.list_projects, methods=['GET', 'POST'])


#TODO check if logged in user is same as the owner of the dash
    def dashboard(self):

        return render_template('dashboard/dashboard.html', user=g.user)

    def profile_view(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        assigned_projects = user.projects
        supervised_projects = Project.query.filter_by(supervisor_id=user.id).all()
        return render_template(
            'dashboard/profile.html',
            user=user,
            assigned_projects=assigned_projects,
            supervised_projects=supervised_projects
        )

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
        return render_template("dashboard/search_users.html", users=users)

    def delete_user(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        project = Project.query.filter_by(supervisor_id=user.id).first()
        form = DeleteUserForm()



        if user == g.user:
            flash("You can't delete your own account!", "danger")
            return redirect(url_for('dashboard.search_users'))

        if form.validate_on_submit():
            if form.terminated.data == 'yes':
                db.session.delete(user)
                db.session.delete(project)
                db.session.commit()
                send_employee_termination_notification(user)
                flash("User has been deleted!", "success")
                return redirect(url_for('dashboard.search_users'))
            else:
                db.session.delete(user)
                db.session.delete(project)
                db.session.commit()
                flash("User has been deleted!", "success")
                return redirect(url_for('dashboard.search_users'))


        return render_template("dashboard/delete_user.html", user=user, form=form)


    def update_user(self, user_id):
        user = User.query.get_or_404(user_id)
        form = UserForm(obj=user)

        if form.validate_on_submit():
            form.populate_obj(user)
            db.session.commit()
            print('updated successfully')
            return redirect(url_for('dashboard.profile_view', user_id=user.id))


        return render_template('dashboard/update_user.html', user=user, form=form)

    # TODO refactor using Flask-WTF #TODO separate projects to own controller
    def create_project(self):
        if request.method == 'POST':
            try:
                name = request.form['name']
                start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d").date()
                finish_date = datetime.strptime(request.form['finish_date'], "%Y-%m-%d").date()
                supervisor_id = request.form['supervisor_id']
                worker_ids = request.form.getlist('workers')

                supervisor = db.session.get(User, supervisor_id)
                workers = [db.session.get(User, int(uid)) for uid in worker_ids]

                new_project = Project(
                    name=name,
                    start_date=start_date,
                    finish_date=finish_date,
                    supervisor=supervisor,
                    assigned_workers=workers
                )

                db.session.add(new_project)
                db.session.commit()
                return render_template('dashboard/dashboard.html', succes=True)

            except SQLAlchemyError as e:
                db.session.rollback()
                flash("Error creating project: " + str(e), "danger")

        all_users = User.query.all()
        return render_template(
            'dashboard/create_project.html',
            supervisors=all_users,
            workers=all_users
        )

    # TODO separate projects to own controller
    def list_projects(self):
        projects = Project.query.all()
        if not projects:
            flash("No projects found!", "danger")
        return render_template('dashboard/list_projects.html', projects=projects)

    # TODO refactor using Flask-WTF
    def time_log(self):
        user_id = g.user.id if g.user else None
        if not user_id:
            return redirect(url_for('auth.login'))

        dates = get_dates_for_current_month()

        if request.method == 'POST':
            for d in dates:
                date_str = d.strftime('%Y-%m-%d')
                start = request.form.get(f'start_{date_str}')
                finish = request.form.get(f'finish_{date_str}')
                log_type = request.form.get(f'type_{date_str}', 'Work')

                if start and finish:
                    try:
                        start_dt = datetime.strptime(start, "%H:%M")
                        finish_dt = datetime.strptime(finish, "%H:%M")
                        total = round((finish_dt - start_dt).seconds / 3600, 2)
                    except ValueError:
                        total = None
                else:
                    total = None

                log = TimeLog.query.filter_by(user_id=user_id, log_date=d).first()
                if not log:
                    log = TimeLog(user_id=user_id, log_date=d)
                    db.session.add(log)

                log.start_time = start
                log.finish_time = finish
                log.total_time = total
                log.log_type = log_type

            db.session.commit()
            return redirect(url_for('dashboard.time_log', user_id=user_id))

        logs = {log.log_date: log for log in TimeLog.query.filter_by(user_id=user_id).all()}
        return render_template('dashboard/time_log.html', dates=dates, logs=logs, current_date=date.today())
