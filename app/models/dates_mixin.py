from app import db
from datetime import datetime

class DateMixin(object):
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime)
    remove_date = db.Column(db.DateTime)