from main.db import db 
from enum import Enum

class Status(Enum):
    ONGOING = 'ONGOING'
    COMPLETED = 'COMPLETED'

class TalaBandi(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='talabandis')
    date = db.Column(db.Date)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.ONGOING)
    end_date = db.Column(db.Date)
    tithi = db.Column(db.String(50))

    def __init__(self, user_id, date, description, status, tithi, end_date=None):
        self.user_id=user_id
        self.date=date
        self.description=description
        self.status=status
        self.end_date=end_date
        self.tithi=tithi