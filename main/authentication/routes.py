from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify
from .utils import *
from datetime import datetime

from main.db import db
from main.Home.models import Status, TalaBandi
from sqlalchemy import desc

authentication = Blueprint("authentication", __name__, template_folder="templates")

@authentication.route("/", methods=['GET','POST'])
@login_not_required
def login():
	if request.method == "POST":
		email = request.form.get("email")
		password = request.form.get("password")

		if email == '' or email is None:
			flash("Email cannot be empty!")
		elif password == '' or password is None:
			flash("Password cannot be empty!")
		elif getUserByEmail(email) is None or getUserByEmail(email) == '':
			flash("Unauthorized access!")
		else:
			session['user'] = email 
			return redirect(url_for('authentication.admin_home'))

	return render_template("login.html")

@authentication.route("/admin/")
@login_required
def admin_home():
	username = getUserByEmail(session['user']).name
	talabandi_list = TalaBandi.query.order_by(desc(TalaBandi.date)).all()
	print(talabandi_list)
	return render_template("admin.html", username=username, talabandi_list=talabandi_list)

@authentication.route('/logout/')
@login_required
def logout():
	session.pop('user', None)
	return redirect(url_for('authentication.admin_home'))

@authentication.route("/add/talabandi/", methods=['POST'])
@login_required
def add_talabandi():
	date = request.form.get("talabandi_date")
	description = request.form.get("description")
	status = request.form.get("status")
	enddate = None

	_enddate = None

	if status == Status.COMPLETED.value:
		enddate = request.form.get("end_date")
		_enddate = strDateToPythonDate(enddate)


	_date = strDateToPythonDate(date)
	tithi = getTithi(_date)

	if date is None or date == '':
		flash("Date cannot be empty")
	elif status is None or status == '':
		flash("Status cannot be empty")
	else:
		if _date>datetime.now().date():
			flash("No future prediction please")
		elif checkTalabandiCollision(_date) and status==Status.ONGOING.value:
			flash("Talabandi date collision occured")
		elif isOngoingTalabandiNotBeforeLastEndTime(_date) and status==Status.ONGOING.value:
			flash("Ongoing cannot be before last talabandi")
		elif isTalabandiOngoing() and status==Status.ONGOING.value:
			flash("Talabandi is already ongoing")
		elif status==Status.COMPLETED.value:
			if TalabandiAlreadyExists(_date, _enddate):	
				flash("Talabandi already exists")
			else:
				save(_date,description,status,tithi,_enddate)
		else:
			save(_date,description,status,tithi, _enddate)		

	return redirect(url_for("authentication.admin_home"))


@authentication.route("/edit/<int:id>", methods=['GET','POST'])
@login_required
def edit_talabandi(id):
	res = TalaBandi.query.filter(TalaBandi.id==id, TalaBandi.status==Status.ONGOING.value).first()
	
	return render_template("edit.html",res=res)

@authentication.route('/delete-talabandi/', methods=['POST'])
def delete_talabandi():
	data = request.json
	talabandi_id = data.get('id')

	# Fetch the TalaBandi instance and delete it
	talabandi = TalaBandi.query.get(talabandi_id)
	print(talabandi)
	if talabandi:
		db.session.delete(talabandi)
		db.session.commit()
		return jsonify({"success": True, "message": "TalaBandi deleted successfully."})
	else:
		return jsonify({"success": False, "message": "TalaBandi not found."})
