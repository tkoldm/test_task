from datetime import datetime
from app import celery, db
from app.calculate_dates import days_to_delete
from app.models.article_model import Article

@celery.task
def mark_article_deleted(id):
    article = Article.query.filter_by(id=id).first()
    if article:
        if not article.remove_date:
            article = Article.query.filter_by(id = id).update({'remove_date': datetime.utcnow()})
            db.session.commit()
            delete_article_from_db.apply_async(args=[id], eta=days_to_delete())

@celery.task
def delete_article_from_db(id):
    article = Article.query.filter_by(id=id).first()
    if article and article.remove_date:
        db.session.delete(article)
        db.session.commit()