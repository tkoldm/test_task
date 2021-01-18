import os

basedir = os.path.abspath(os.path.dirname(__file__))
ARTICLES_PER_PAGE = 5

class Config(object):
    SECRET_KEY = 'AAA'

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:12345@localhost/ad_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    