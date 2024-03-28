import sqlite3
from main.authentication.utils import hashPassword
from datetime import datetime
import os

def create():
	db_path = os.path.join(os.getcwd(), "db")

	# Connect to the SQLite database
	connection = sqlite3.connect(f"{db_path}/db.sqlite3")

	# Create a cursor object
	cursor = connection.cursor()

	# Insert data into the database
	password = hashPassword('admin')
	now = datetime.now()

	email = 'admin@a.com'
	cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE email = ?)", (email,))
	exists = cursor.fetchone()[0]

	if not exists:

		cursor.execute("INSERT INTO users (name, email, password, created_at, updated_at) VALUES (?, ?, ?, ?, ?)", ('Admin', 'admin@a.com', password, now, now))
		# Commit the changes and close the connection
		connection.commit()
		connection.close()