from flask import (
    Blueprint, render_template, request, session, redirect, url_for
)
from sqlalchemy.orm import joinedload

from polygonerp.TimeLog import TimeLog
from . import db
from datetime import date, timedelta, datetime
from polygonerp.user import User
from .project import Project


def get_dates_for_current_month():
    today = date.today()
    first_day = date(today.year, today.month, 1)
    next_month = date(today.year + int(today.month / 12), (today.month % 12) + 1, 1)
    delta = (next_month - first_day).days

    return [first_day + timedelta(days=i) for i in range(delta)]

bp = Blueprint('dash', __name__, url_prefix='/dash')

class DashboardController:

    @staticmethod
    @bp.route('/dashboard/<user_id>', methods=('GET', 'POST'))
    def dashboard(user_id):
        user = User.query.filter_by(id=user_id).first()
        name = user.name
        is_admin = user.is_admin
        print(user)

        return render_template('dash/dashboard.html', name=name, is_admin=is_admin)

    @staticmethod
    @bp.route('/profile/<user_id>', methods=('GET', 'POST'))
    def profile_view(user_id):
        #user = User.query.filter_by(id=user_id).first()
        user = User.query.filter_by(id=user_id).first()

        assigned_projects = user.projects  # many-to-many
        supervised_projects = Project.query.filter_by(supervisor_id=user.id).all()

        return render_template(
            'dash/profile.html',
            user=user,
            assigned_projects=assigned_projects,
            supervised_projects=supervised_projects
        )

#TODO modify like reg request.form
    @staticmethod
    @bp.route('/search', methods=('GET', 'POST'))
    def search_users():
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

        users = User.query.filter(*filters).all() if filters else []

        return render_template("dash/search_users.html", users=users)




    @staticmethod
    @bp.route('<user_id>/log', methods=['GET', 'POST'])
    def time_log(user_id):
        user_id = session.get('id')  # assuming session stores the current user id
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

                # find or create log
                log = TimeLog.query.filter_by(user_id=user_id, log_date=d).first()
                if not log:
                    log = TimeLog(user_id=user_id, log_date=d)
                    db.session.add(log)

                log.start_time = start
                log.finish_time = finish
                log.total_time = total
                log.log_type = log_type

            db.session.commit()
            return redirect(url_for('dash.time_log'))

        # Load existing logs
        logs = {log.log_date: log for log in TimeLog.query.filter_by(user_id=user_id).all()}
        return render_template('dash/time_log.html', dates=dates, logs=logs, current_date=date.today())






