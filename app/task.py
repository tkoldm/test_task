from datetime import datetime
from app import celery, db
from app.article_model import Article

@celery.task
def mark_article_deleted(id):
    article = Article.query.filter_by(id=id).first()
    if article:
        if not article.remove_date:
            article = Article.query.filter_by(id = id).update({'remove_date': datetime.utcnow()})
            db.session.commit()
            delete_article_from_db.apply_async(args=[article.id], countdown=600)

@celery.task
def delete_article_from_db(id):
    article = Article.query.filter_by(id=id).first()
    if article:
        if not article.remove_date:
            db.session.delete(article)
            db.session.commit()