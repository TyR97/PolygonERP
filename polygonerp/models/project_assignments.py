from polygonerp.db import db
"""
Association table for assigning users to projects.
"""
project_assignments = db.Table(
    'project_assignments',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
)
