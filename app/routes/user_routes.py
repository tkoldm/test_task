# -*- coding: utf-8 -*-
from datetime import datetime
from flask import request, jsonify, g
from flask_login import current_user, login_user, logout_user, login_required
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.auth import basic_auth
from app import app, db, login
from config import ARTICLES_PER_PAGE
from app.models.article_model import Article
from app.models.role_model import Role
from app.models.user_model import User
from app.errors import error_response

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/api/authorization', methods=['POST'])
def authorization():
    
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user:
        if not user.remove_date:
            if user.password == password:
                g.current_user = user
                login_user(user, remember=True)
                print(current_user.is_authenticated)
                return jsonify({'Success':'User has been authenticated'})
            else:
                return error_response(404, 'Wrong password')
        else:
            return error_response(410, 'Deleted user')
    else:
        return error_response(404, "Incorrect data")


@app.route('/api/profile/<int:id>')
def user_profile(id):
    page = request.args.get('page', 1, type=int)
    sort_type = request.args.get('sort_by', 'date', type=str)
    
    user = User.query.filter_by(id=id).first_or_404()
    if sort_type == 'date':
        articles = Article.query.order_by(Article.create_date.desc()).filter_by(user=id).paginate(page, ARTICLES_PER_PAGE, False)
    elif pole == 'title':
        articles = Article.query.order_by(Article.title.desc()).filter_by(user=id).paginate(page, ARTICLES_PER_PAGE, False)
    elif pole == 'update':
        articles = Article.query.order_by(Article.update_date.desc()).filter_by(user=id).paginate(page, ARTICLES_PER_PAGE, False)
    articles_to_template = []
    for article in articles.items:
        if not article.remove_date:
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


@app.route('/api/logout', methods=['POST'])
def logout():
    if g.current_user.is_authenticated:
        logout_user()
    return jsonify({'Success':'User has been logouted'})


@app.route('/api/registration', methods=['POST'])
def registration():
    name = request.json['u_name']
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if user:
        return error_response(400, 'User has already registered')

    new_user = User(name=name, username=username, password=password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'Success':'User has been registered'})