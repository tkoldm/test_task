from datetime import datetime, timedelta
from config import DAYS_TO_END

def days_to_mark(end_date):
    date_mark = end_date + timedelta(days=10)
    return date_mark

def days_to_delete():
    date_delete = datetime.utcnow() + timedelta(days=30)
    return date_delete

def calculate_end_date():
    end_date = datetime.utcnow() + timedelta(days=DAYS_TO_END)
    return end_date

def check_dates(date):
    if datetime.utcnow() > date:
        return False
    return True