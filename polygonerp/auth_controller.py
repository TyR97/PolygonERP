

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Message
from polygonerp.user import User
from polygonerp.db import db
from docx import Document


class AuthController:
        def __init__(self, blueprint, app):
            self.bp = blueprint
            app.before_request(self.load_logged_in_user)
            self.bp.add_url_rule('/register', view_func=self.register, methods=['GET', 'POST'])
            self.bp.add_url_rule('/login', view_func=self.login, methods=['GET', 'POST'])
            self.bp.add_url_rule('/logout', view_func=self.logout)
            self.existing_usernames = []

        def generate_username(self, full_name):
            parts = full_name.split(' ')
            if len(parts) < 2:
                raise   ValueError("Full name must have at least two words")

            last_name = parts[0].capitalize()
            first_name = parts[1].capitalize()
            base_username = f"{last_name}{first_name[0]}"

            username = base_username
            counter = 1

            while username in self.existing_usernames:
                username = f"{base_username}{counter}"
                counter += 1
            self.existing_usernames.append(username)
            return username

        def load_logged_in_user(self):
            user_id = session.get('user_id')
            g.user = User.query.filter_by(id=user_id).first() if user_id else None

        def register(self):
            from polygonerp import mail


            if request.method == 'POST':
                #username = request.form['username']
                password_hash = request.form['password']
                name = request.form['name']
                maiden_name = request.form['maiden_name']
                mothers_name = request.form['mothers_name']
                pob = request.form['pob']
                dob = request.form['dob']
                address = request.form['address']
                tax_num = request.form['tax_num']
                taj_number = request.form['taj_number']
                job_title = request.form['job_title']
                base_pay = request.form['base_pay']
                is_admin = job_title.lower() == 'dev'
                print(request.form)

                error = None

                #TODO check fields

                if error is None:
                    try:
                        username = self.generate_username(name)
                        user_mail = username+"@novirusmail.com"
                        new_user = User(
                            username=username,
                            password_hash=generate_password_hash(password_hash),
                            name=name,
                            maiden_name=maiden_name,
                            mothers_name=mothers_name,
                            pob=pob,
                            dob=dob,
                            address=address,
                            tax_num=tax_num,
                            taj_number=taj_number,
                            job_title=job_title,
                            base_pay=base_pay,
                            email_address=user_mail,
                            is_admin=is_admin
                        )
                        db.session.add(new_user)
                        db.session.commit()

                        doc = Document("employee_contract_template.docx")

                        for p in doc.paragraphs:
                            if '{name}' in p.text:
                                p.text = p.text.replace('{name}', new_user.name)
                            if '{maiden_name}' in p.text:
                                p.text = p.text.replace('{maiden_name}', new_user.maiden_name)
                            if  '{mothers_name}' in p.text:
                                p.text = p.text.replace('{mothers_name}', new_user.mothers_name)
                            if '{pob}' in p.text:
                                p.text = p.text.replace('{pob}', new_user.pob)
                            if '{dob}' in p.text:
                                p.text = p.text.replace('{dob}', str(new_user.dob))
                            if '{address}' in p.text:
                                p.text = p.text.replace('{address}', str(new_user.address))
                            if '{tax_num}' in p.text:
                                p.text = p.text.replace('{tax_num}', str(new_user.tax_num))
                            if '{taj_number}' in p.text:
                                p.text = p.text.replace('{taj_number}', str(new_user.taj_number))
                            if '{job_title}' in p.text:
                                p.text = p.text.replace('{job_title}', new_user.job_title)
                            if '{base_pay}' in p.text:
                                p.text = p.text.replace('{base_pay}', str(new_user.base_pay))
                        doc.save(f"{new_user.name}_contract.docx")

                    except Exception as e:
                        db.session.rollback()
                        print(f"Error adding user: {e}")
                        error = str(e)
                    else:
                        return redirect(url_for('auth.login'))


                msg = Message(f'Új alkalmazott felvétele: {name}',
                              sender='postmaster@sandbox0ce297070b444e6ea390aba06950b419.mailgun.org',
                              recipients=['cik7nj@gmail.com'])
                msg.body = f"""Kedves kollégák kérem az alábbi új alkalmazott bejelentését.
                Új alkalmazott adatai:
                Név: {name}
                Szül. Név: {maiden_name}
                Szül. hely: {pob}
                Szül. idő: {dob}
                Anyja neve: {mothers_name}
                Lakcím: {address}
                Adószám: {tax_num}
                Taj szám: {taj_number}
                Pozíció: {job_title}
                Alapbér: {base_pay}
                
                Üdvözlettel,
                ERP SYS ADMIN
        """

                # E-mail küldése
                try:
                    mail.send(msg)
                    return "Az e-mail sikeresen elküldve!"
                except Exception as e:
                    return f"Hiba történt az e-mail küldésekor: {str(e)}"





            return render_template('auth/register.html')


        def login(self):
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']


                user = User.query.filter_by(username=username).first()
                print(user)

                error = None

                if user is None:
                    error = "Incorrect username."
                elif not check_password_hash(user.password_hash, password):
                    error = "Incorrect password."

                if error is None:
                    session['id'] = user.id
                    print(session['id'])
                    return redirect(url_for('dash.dashboard', user_id = user.id))
                print(error)
            return render_template('auth/login.html')

        def logout(self):
            session.clear()
            return redirect(url_for('index'))


bp = Blueprint('auth', __name__, url_prefix='/auth')
def init_auth_controller(app):
    AuthController(bp, app)

'''
@bp.before_app_request


#@bp.route('/logout')
'''

'''
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
'''