from main.db import db
from datetime import datetime

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100), nullable=False, unique=True)
	password = db.Column(db.String(100), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.now)
	updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

	def __init__(self, name, email, username, password,is_superuser=None):
		self.name = name
		self.email = email
		self.password = password