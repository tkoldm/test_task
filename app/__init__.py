from flask import Flask, Blueprint, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import logging
from celery import Celery
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

celery = Celery(app, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

login = LoginManager(app)
login.init_app(app)

from app.routes import user_routes 
from app.routes import article_routes
from app.admin.admin_model import AdminView, IndexView
from app.admin import admin_routes
from app.models.user_model import User
from app.models.article_model import Article
from app.models.role_model import Role
from app.routes.user_routes import user_blueprint
from app.routes.article_routes import article_blueprint

app.register_blueprint(user_blueprint, url_prefix='/api/user')
app.register_blueprint(article_blueprint, url_prefix='/api/article')

admin = Admin(app, index_view=IndexView())
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))
admin.add_view(AdminView(Article, db.session))


