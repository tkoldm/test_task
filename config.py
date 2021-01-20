import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
ARTICLES_PER_PAGE = 5

class Config(object):
    load_dotenv()
    
    SECRET_KEY = 'AAA'

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')

    