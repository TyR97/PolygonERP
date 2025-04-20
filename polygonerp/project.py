from polygonerp.db import db
from polygonerp.project_assignments import project_assignments


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    finish_date = db.Column(db.Date, nullable=False)

    supervisor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    supervisor = db.relationship('User', foreign_keys=[supervisor_id])

    assigned_workers = db.relationship(
        'User',
        secondary=project_assignments,
        backref='projects'
    )

    def __repr__(self):
        return f"<Project {self.name}>"