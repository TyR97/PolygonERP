import os

from flask import render_template, request, redirect, url_for, flash, g
from datetime import date, datetime
from flask import current_app
from werkzeug.utils import send_from_directory

from polygonerp.models.time_log import TimeLog
from polygonerp.models.user import User
from polygonerp.db import db
from polygonerp.models.project import Project
from polygonerp.utils.decorators_util import login_required
from polygonerp.utils.date_utils import  get_dates_for_current_month
from polygonerp.utils.doc_utils import find_user_contract, time_log_to_doc


class DashboardController:
    def __init__(self, blueprint, app):
        self.bp = blueprint
        # Registering routes for Blueprint
        self.bp.add_url_rule('/', view_func=login_required(self.dashboard), methods=['GET', 'POST'])
        self.bp.add_url_rule('/profile/<user_id>', view_func=login_required(self.profile_view), methods=['GET', 'POST'])
        self.bp.add_url_rule('/download_contract/<user_id>', view_func=login_required(self.download_contract), methods=['GET', 'POST'])
        self.bp.add_url_rule('/download_log/<user_id>', view_func=login_required(self.download_log), methods=['GET', 'POST'])
        self.bp.add_url_rule('/log', view_func=self.time_log, methods=['GET', 'POST'])

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

    def download_contract(self, user_id):
        user = User.query.get_or_404(user_id)
        if user == g.user or g.user.is_admin:
            try:
                return find_user_contract(user)
            except FileNotFoundError as e:
                flash(str(e), 'danger')
                return redirect(url_for('dashboard.profile_view', user_id=user_id))
        else:
            return redirect(url_for('dashboard.profile_view', user_id=user_id))

    def download_log(self, user_id):
        user = User.query.get_or_404(user_id)
        logs = TimeLog.query.filter_by(user_id=user_id).all()
        if user == g.user or g.user.is_admin:
            if user and logs:
                return time_log_to_doc(logs, user.name)
            elif not logs:
                flash("No time sheet found", "danger")
                return redirect(url_for('dashboard.profile_view', user_id=user_id))


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
