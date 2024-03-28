from .models import TalaBandi, Status

def isTalabandi():
    return True if TalaBandi.query.filter(TalaBandi.status==Status.ONGOING).first() else False