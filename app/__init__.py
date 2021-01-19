from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from celery import Celery
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

celery = Celery(app, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

login = LoginManager(app)
login.init_app(app)

from app import user_routes 
from app import article_routes
from app.admin_model import AdminView
from app import admin_routes
from app.user_model import User
from app.article_model import Article
from app.role_model import Role

admin = Admin(app)#, index_view=AdminView(name='home'))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))
admin.add_view(AdminView(Article, db.session))


