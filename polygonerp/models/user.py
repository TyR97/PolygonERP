from polygonerp.db import db

"""
employee user in the PolygonERP system
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), unique = True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    maiden_name = db.Column(db.String(200), nullable=False)
    mothers_name = db.Column(db.String(200), nullable=False)
    pob = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    tax_num = db.Column(db.String(10), unique=True ,nullable=False)
    taj_number = db.Column(db.String(10), unique=True, nullable=False)
    job_title = db.Column(db.String(200), nullable=False)
    base_pay = db.Column(db.Integer, nullable=False)
    email_address = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    first_login = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<User %r>' % self.username