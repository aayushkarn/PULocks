from flask import Flask
from .config import Config
from .db import init_db
from .create_superuser import create

from main.authentication.routes import authentication
from main.Home.routes import home

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	init_db(app)
	create()

	app.register_blueprint(authentication, url_prefix="/auth/")
	app.register_blueprint(home, url_prefix="/")

	return app
