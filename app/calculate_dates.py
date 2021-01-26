from datetime import datetime, timedelta

def days_to_mark():
    date_mark = datetime.utcnow() + timedelta(days=10)
    return date_mark

def days_to_delete():
    date_delete = datetime.utcnow() + timedelta(days=30)
    return date_delete