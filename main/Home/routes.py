from datetime import datetime
from main.authentication.utils import getLastTalabandi
from flask import Blueprint, render_template, url_for, request, flash
from .utils import *

from main.authentication.utils import getTithi
from sqlalchemy import desc

home = Blueprint("home", __name__, template_folder="templates")

@home.route("/", methods=['GET','POST'])
def index():
	# if request.method == "POST":
	# 	email = request.form.get("email")
	# 	password = request.form.get("password")

	# 	if email == '' or email is None:
	# 		flash("Email cannot be empty!")
	# 	elif password == '' or password is None:
	# 		flash("Password cannot be empty!")
	# 	elif getUserByEmail(email) is None or getUserByEmail(email) == '':
	# 		flash("Unauthorized access!")
	# 	else:
	# 		pass
	# 		print(email, password)
	talaState = isTalabandi()
	tithi = getTithi(datetime.now().date())
	return render_template("index.html", isTalabandi=talaState, tithi=tithi)

@home.route('/about/')
def about():
	return render_template('about.html')

@home.route('/stats/')
def stats():
	last = getLastTalabandi()
	stat=isTalabandi()
	ongoing = TalaBandi.query.filter(TalaBandi.status==Status.ONGOING).first()
	talabandi_list = TalaBandi.query.filter(TalaBandi.status!=Status.ONGOING).order_by(desc(TalaBandi.date)).all()
	return render_template('stats.html', last=last, isTalabandi=stat, talabandi_list=talabandi_list, ongoing=ongoing)
	