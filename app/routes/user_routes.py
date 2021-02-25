# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Blueprint, request, jsonify, g
from flask_login import current_user, login_user, logout_user, login_required
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.auth import basic_auth
from app import app, db, login, logger
from config import ARTICLES_PER_PAGE
from app.models.article_model import Article
from app.models.role_model import Role
from app.models.user_model import User
from app.errors import error_response
from app.queries import check_user_login, check_user_registration, get_articles_by_user

user_blueprint = Blueprint('user_blueprint', __name__)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@user_blueprint.route('/authorization', methods=['POST'])
def authorization():
    
    username = request.json['username']
    password = request.json['password']
    user = check_user_login(username, password)
    login_user(user, remember=True)
    logger.info(f'user:{current_user.username} - logged in')
    return jsonify({'Success':'User login'})


@user_blueprint.route('/profile/<int:id>')
def user_profile(id):
    page = request.args.get('page', 1, type=int)
    on_page = request.args.get('on_page', ARTICLES_PER_PAGE, type=int)
    sort_type = request.args.get('sort_by', 'date', type=str)
    
    if sort_type == 'date':
        articles = get_articles_by_user(Article.create_date, id, page, on_page)
    elif pole == 'title':
        articles = get_articles_by_user(Article.title, id, page, on_page)
    elif pole == 'update':
        articles = get_articles_by_user(Article.update_date, id, page, on_page)
    articles_to_template = []
    for article in articles.items:
        obj = {
            'id': article.id,
            'create_date': article.create_date,
            'update_date': article.update_date,
            'remove_date': article.remove_date,
            'user': article.user,
            'title': article.title,
            'body': article.body,
            'end_date': article.end_date
        }
        articles_to_template.append(obj)
    return jsonify({'articles':articles_to_template})


@user_blueprint.route('/change_password', methods=['POST'])
@basic_auth.login_required
def change_password():
    new_password = request.json['password']
    current_user.set_password(new_password)
    db.session.commit()
    logger.info(f'user:{current_user.username} - changed password')
    return jsonify({'Success':'Password has been changed'})

@user_blueprint.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return jsonify({'Success':'User has been logouted'})


@user_blueprint.route('/registration', methods=['POST'])
def registration():
    name = request.json['u_name']
    username = request.json['username']
    password = request.json['password']

    user = check_user_registration(username)

    if user:
        return error_response(400, 'User has already registered')

    new_user = User(name=name, username=username)
    new_user.set_password(password)

    login_user(new_user)

    db.session.add(new_user)
    db.session.commit()
    logger.info(f'user:{username} - has been registred')
    return jsonify({'Success':'User has been registered'})