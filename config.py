import os

basedir = os.path.abspath(os.path.dirname(__file__))
ARTICLES_PER_PAGE = 5

class Config(object):
    SECRET_KEY = 'AAA'

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or "postgresql://postgres:12345@localhost/ad_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379'

    