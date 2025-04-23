from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, flash
)
from flask_wtf import form
from sqlalchemy.sql.functions import current_user
from werkzeug.security import check_password_hash, generate_password_hash

from polygonerp.models import user
from polygonerp.models.user import User
from polygonerp.db import db
from polygonerp.templates.forms.PasswordChange import ChangePasswordForm
from polygonerp.templates.forms.user_form import UserForm

from polygonerp.utils.auth_utils import generate_username, generate_password
from polygonerp.utils.email_utils import send_new_employee_notification, send_firs_login_notification
from polygonerp.utils.doc_utils import create_contract


class AuthController:
        def __init__(self, blueprint, app):
            self.bp = blueprint
            app.before_request(self.load_logged_in_user)
            self.bp.add_url_rule('/register', view_func=self.register, methods=['GET', 'POST'])
            self.bp.add_url_rule('/login', view_func=self.login, methods=['GET', 'POST'])
            self.bp.add_url_rule('/change_password', view_func=self.change_password, methods=['GET', 'POST'])
            self.bp.add_url_rule('/logout', view_func=self.logout)

            self.existing_usernames = []



        def load_logged_in_user(self):
            user_id = session.get('user_id')
            g.user = User.query.filter_by(id=user_id).first() if user_id else None

        def register(self):
            admin_titles = ['senior developer', 'hr', 'accountant', 'sysadmin', 'dev']
            form = UserForm()

            if request.method == 'POST' and form.validate_on_submit():
                username = generate_username(self.existing_usernames, form.name.data)
                password = generate_password()
                user_mail = username + "@polygon_erp.com"
                is_admin = form.job_title.data.lower() in admin_titles

                new_user = User(
                    username=username,
                    password_hash=generate_password_hash(password),
                    name=form.name.data,
                    maiden_name=form.maiden_name.data,
                    mothers_name=form.mothers_name.data,
                    pob=form.pob.data,
                    dob=form.dob.data,
                    address=form.address.data,
                    tax_num=form.tax_num.data,
                    taj_number=form.taj_number.data,
                    job_title=form.job_title.data,
                    base_pay=form.base_pay.data,
                    email_address=user_mail,
                    is_admin=is_admin
                )

                try:
                        db.session.add(new_user)
                        db.session.commit()
                        create_contract(new_user)
                        send_new_employee_notification(new_user)
                        send_firs_login_notification(new_user, password)
                except Exception as e:
                    db.session.rollback()
                    print(f"Error adding user: {e}")
                else:
                    return redirect(url_for('auth.login'))

            return render_template('auth/register.html', form=form)


        def login(self):
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                user = User.query.filter_by(username=username).first()
                session['user_id'] = user.id
                if user.first_login:
                    print("first login")
                    return redirect(url_for('auth.change_password'))
                print(user)

                error = None

                if user is None:
                    error = "Incorrect username."
                elif not check_password_hash(user.password_hash, password):
                    error = "Incorrect password."
                    print(error)

                if error is None:
                    session['user_id'] = user.id
                    return redirect(url_for('dashboard.dashboard'))
                print(error)
            return render_template('auth/login.html')

        def logout(self):
            session.clear()
            return redirect(url_for('index'))


        def change_password(self):
            print("beléptünk a fv.be")
            form = ChangePasswordForm()
            user = User.query.filter_by(id=session['user_id']).first()
            print(user)

            if form.validate_on_submit():
                user.password_has = generate_password_hash(form.password.data)
                user.first_login = False
                db.session.commit()
                return redirect(url_for('dashboard.dashboard'))

            return render_template('auth/new_password.html', form=form)  # <-- this line fixes the error


bp = Blueprint('auth', __name__, url_prefix='/auth')
def init_auth_controller(app):
    AuthController(bp, app)
