from main.Home.models import TalaBandi, Status
from flask  import session, redirect, url_for
from functools import wraps
import hashlib
from datetime import datetime
import nepali_datetime

from .models import User
from main.db import db
from main.tithi.scraper import Scraper

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session or session['user'] == "":
            return redirect(url_for('authentication.login'))
        return func(*args, **kwargs)
    return wrapper

def login_not_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return redirect(url_for('authentication.admin_home'))
        return func(*args, **kwargs)
    return wrapper

salt = b'cd62a18e82c040db8faff500eabaf29e'

def hashPassword(password):
    newPass = password.encode('utf-8')+salt
    hashedPass = hashlib.sha256(newPass).hexdigest()
    return hashedPass

def verifyPassword(password, userPass):
    newPass = hashPassword(password)
    if newPass == userPass:
        return True
    return False

def getUserByEmail(email):
    return User.query.filter_by(email=email).first()

def strDateToPythonDate(date):
    if date is not '':
        return datetime.date(datetime.strptime(date, '%Y-%m-%d'))

def adToBs(date):
    ad_date = date
    bs_date = nepali_datetime.date.from_datetime_date(ad_date)
    return bs_date

def getTithi(date):
    _date = adToBs(date)
    s = Scraper(_date.year, _date.month, _date.day)
    return s.get_tithi()

def isTalabandiOngoing():
    a = TalaBandi.query.filter(TalaBandi.status==Status.ONGOING).first()
    if a is not None:
        return True
    else:
        return False
    
def getLastTalabandi():
    return TalaBandi.query.order_by(TalaBandi.end_date.desc()).first() 

def isOngoingTalabandiNotBeforeLastEndTime(starttime):
    last = getLastTalabandi()
    print(last)
    if last is not None:
        if starttime<last.end_date:
            return True
        else:
            return False
    else:
        return False

def checkTalabandiCollision(startdate):
    if TalaBandi.query.filter(TalaBandi.date>=startdate, TalaBandi.end_date<=startdate).first() is not None:
        return True
    else:
        return False

def TalabandiAlreadyExists(startdate,enddate):
    if startdate is None or enddate is None:
        raise Exception("Date cannot be none")
    if TalaBandi.query.filter(TalaBandi.date<=startdate, TalaBandi.end_date>=enddate, TalaBandi.status==Status.COMPLETED).first() is not None:
        print(1)
        return True
    # elif TalaBandi.query.filter(TalaBandi.date<=startdate, TalaBandi.end_date<=enddate, TalaBandi.status==Status.COMPLETED).first() is not None:
    #     print(2)
    #     print(TalaBandi.query.filter(TalaBandi.date<=startdate, TalaBandi.end_date<=enddate, TalaBandi.status==Status.COMPLETED).first())
    #     return True
    # elif TalaBandi.query.filter(TalaBandi.date>=startdate, TalaBandi.end_date>=enddate, TalaBandi.status==Status.COMPLETED).first() is not None:
    #     print(3)
    #     return True
    elif TalaBandi.query.filter(TalaBandi.date<=startdate, TalaBandi.end_date>=enddate, TalaBandi.status==Status.COMPLETED).first() is not None:
        print(4)
        return True
    else:
        return False

def save(date, description,status, tithi, enddate=None):
    user = getUserByEmail(session['user'])
    t = TalaBandi(user_id=user.id, date=date, description=description, status=status,tithi=tithi, end_date=enddate)
    db.session.add(t)
    db.session.commit()