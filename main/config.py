import os

db_dir = os.path.join(os.getcwd(), "db")
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
db_path = os.path.join(os.getcwd(), "db")

class Config:
    DEBUG = True
    SECRET_KEY = "923e6ceed5ff4f0aba7df1cb1a701dc3"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db.sqlite3'.format(db_path)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/'))

