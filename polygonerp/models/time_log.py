from polygonerp.db import db
from sqlalchemy.orm import relationship
"""
Represents a log entry for tracking user work hours and activity.
"""

class TimeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    log_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(10), nullable=True)
    finish_time = db.Column(db.String(10), nullable=True)
    total_time = db.Column(db.Float, nullable=True)
    log_type = db.Column(db.String(20), nullable=False, default='Work')

    user = relationship("User", backref="time_logs")

    def __repr__(self):
        return f"<TimeLog {self.user_id} - {self.log_date}>"
