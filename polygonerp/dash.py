from flask import (
    Blueprint, render_template, request, session, g
)
from flask_mail import Message
from . import mail
from polygonerp.user import User

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
        user = User.query.filter_by(id=user_id).first()
        return render_template('dash/profile.html', user=user)


