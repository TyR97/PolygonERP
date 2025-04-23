from datetime import datetime

from flask_mail import Message

def send_new_employee_notification(user):
    from polygonerp import mail
    subject = f'Új alkalmazott felvétele: {user.name}'
    recipients = ['cik7nj@gmail.com']  # you can make this a parameter if you want it flexible
    sender = 'postmaster@sandbox0ce297070b444e6ea390aba06950b419.mailgun.org'

    body = f"""Kedves kollégák, kérem az alábbi új alkalmazott bejelentését.

Új alkalmazott adatai:
Név: {user.name}
Szül. Név: {user.maiden_name}
Szül. hely: {user.pob}
Szül. idő: {user.dob}
Anyja neve: {user.mothers_name}
Lakcím: {user.address}
Adószám: {user.tax_num}
Taj szám: {user.taj_number}
Pozíció: {user.job_title}
Alapbér: {user.base_pay}

Üdvözlettel,
ERP SYS ADMIN
"""

    msg = Message(subject, sender=sender, recipients=recipients, body=body)

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False


def send_employee_termination_notification(user):
    from polygonerp import mail
    subject = f'Alkalmazott munkaviszonyának megszünése: {user.name}'
    recipients = ['cik7nj@gmail.com']  # you can make this a parameter if you want it flexible
    sender = 'postmaster@sandbox0ce297070b444e6ea390aba06950b419.mailgun.org'

    body = f"""Kedves kollégák, kérem az alábbi alkalmazott munkaviszonyának megszüntetését a mai nappal ({datetime.today()}).

Alkalmazott adatai:
Név: {user.name}
Adószám: {user.tax_num}
Taj szám: {user.taj_number}

Üdvözlettel,
ERP SYS ADMIN
"""

    msg = Message(subject, sender=sender, recipients=recipients, body=body)

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False


def send_firs_login_notification(user, password):
    from polygonerp import mail
    subject = f'{user.name} Polygon_ERP első belépés'
    recipients = ['cik7nj@gmail.com']  # you can make this a parameter if you want it flexible
    sender = 'postmaster@sandbox0ce297070b444e6ea390aba06950b419.mailgun.org'

    body = f"""Kedves kolléga, üdvőzlöm a Polygon_ERP rendszerben.


Név: {password}

Üdvözlettel,
ERP SYS ADMIN
"""

    msg = Message(subject, sender=sender, recipients=recipients, body=body)

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False