from app import db
from app.models.user_model import User
from app.models.article_model import Article

def check_user_login(username, password):
    query = User.query.filter_by(username=username).filter_by(password=password).filter_by(remove_date=None).first()
    if query:
        return query
    else:
        return False

def check_user_registration(username):
    query = User.query.filter_by(username=username).first()
    if query:
        return query
    else:
        return False

def get_articles_by_user(row, user_id, page, on_page):
    return Article.query.order_by(row.desc()).filter_by(user=user_id).filter_by(remove_date=None).paginate(page, on_page, False)

def get_articles(row, page, on_page):
    return Article.query.order_by(row.desc()).filter_by(remove_date=None).paginate(page, on_page, False)
