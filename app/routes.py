# -*- coding: utf-8 -*-
from datetime import datetime
from app import app, db, login
from config import ARTICLES_PER_PAGE
from app.articles import Article
from app.role import Role
from app.user import User
from flask import render_template, url_for, request, redirect, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


@app.route('/')
def index():
    return redirect(url_for('articles_list'))


@app.route('/api/articles')
@app.route('/api/articles/page_<int:page>')
def articles_list(page=1):
    articles = Article.query.order_by(Article.create_date.desc()).paginate(page, ARTICLES_PER_PAGE, False)
    articles_to_template = []
    for article in articles.items:
        if not article.remove_date:
            user = User.query.filter_by(id=article.user).first()
            obj = {
                'id': article.id,
                'create_date': article.create_date,
                'update_date': article.update_date,
                'remove_date': article.remove_date,
                'user_id': article.user,
                'username': user.username,
                'title': article.title,
                'body': article.body,
                'end_date': article.end_date
            }
            articles_to_template.append(obj)
    return jsonify({'articles': articles_to_template})


@app.route('/api/articles/sort_<string:pole>')
def article_sort(pole):
    if pole == 'title':
        articles = Article.query.order_by(Article.title.desc()).all()
    elif pole == 'update':
        articles = Article.query.order_by(Article.update_date.desc()).all()
    elif pole == 'user':
        articles = Article.query.order_by(Article.user.desc()).all()
    articles_to_template = []
    for article in articles:
        if not article.remove_date:
            user = User.query.filter_by(id=article.user).first()
            obj = {
                'id': article.id,
                'create_date': article.create_date,
                'update_date': article.update_date,
                'remove_date': article.remove_date,
                'user_id': article.user,
                'username': user.username,
                'title': article.title,
                'body': article.body,
                'end_date': article.end_date
            }
            articles_to_template.append(obj)
    return jsonify({'artciles':articles_to_template})


@app.route('/api/articles/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def article_detail(id):
    user_id = request.json['user_id']
    if request.method == 'GET':
        article = Article.query.get(id)
        if article.remove_date:
            return jsonify({'Error':'Article has been deleted'})
        user = User.query.get(article.user)
        obj = {
                'id': article.id,
                'create_date': article.create_date,
                'update_date': article.update_date,
                'remove_date': article.remove_date,
                'user_id': article.user,
                'username': user.username,
                'title': article.title,
                'body': article.body,
                'end_date': article.end_date
            }
        return jsonify({'article':obj})
    
    elif request.method == 'PUT':
        try:
            article = Article.query.get(id)
        except:
            return jsonify({'Error':'Article doesn\'t exist'})
        
        user = User.query.filter_by(id=user_id).first()

        if not user.remove_date:
            if user_id == article.user:
                if not article.remove_date:
                    article = Article.query.filter_by(id = id).update({'update_date': datetime.utcnow()})
                    db.session.commit()
                    return jsonify({'Success':'Article has been updated'})
                else:
                    return jsonify({'Error':'Article deleted'})
            else:
                return jsonify({'Error':'Atricle from another user'})
        else:
            return jsonify({'Error':'Deleted user'})

    else:
        try:
            article = Article.query.get(id)
        except:
            return jsonify({'Error':'Article doesn\'t exist'})
        
        user = User.query.filter_by(id=user_id).first()

        if not user.remove_date:
            if user_id == article.user:
                if not article.remove_date:
                    article = Article.query.filter_by(id = id).update({'remove_date': datetime.utcnow()})
                    db.session.commit()
                    return jsonify({'Error':'Article deleted'})
                else:
                    return jsonify({'Error':'Article already deleted'})
            else:
                return jsonify({'Error':'Atricle from another user'})
        else:
            return jsonify({'Error':'Deleted user'})


@app.route('/api/add_article', methods=['POST'])
def add_new_article():
    if not request.json:
        return jsonify({'Error':'Incorrect type'})
    
    user_id = request.json['user_id']

    user = User.query.filter_by(id=user_id).first()
    if user:
        if not user.remove_date:

            title = request.json['title']
            body = request.json['body']
            
            article = Article(title=title, body=body, user=user_id)
            
            db.session.add(article)
            db.session.commit()
        
            return jsonify({'Success':'Artlicle has been added'})

        else:
            return jsonify({'Error':f'User {user.username} has been blocked'}, 404)
    else:
        return jsonify({'Error':'Unregistred user'})


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/api/authorization', methods=['POST'])
def authorization():
    if current_user.is_authenticated:
        return jsonify({'Error':'User already authenticated'})
    
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()
    if user:
        if not user.remove_date:
            if user.password == password:
                login_user(user, remember=True)
                print(current_user.is_authenticated)
                return jsonify({'Success':'User has been authenticated'})

            else:
                return jsonify({"Error":"Deleted user"})
    else:
        return jsonify({"Error":"Incorrect data"})


@app.route('/api/profile/<int:id>')
@app.route('/api/profile/<int:id>/page_<int:page>')
def user_profile(id, page=1):
    user = User.query.filter_by(id=id).first_or_404()
    articles = Article.query.order_by(Article.create_date.desc()).filter_by(user=id).paginate(page, ARTICLES_PER_PAGE, False)
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


@app.route('/api/profile/<int:id>/sort_<string:pole>')
def user_profile_sort(id, pole):
    user = User.query.filter_by(id=id).first_or_404()
    if pole == 'title':
        articles = Article.query.order_by(Article.title.desc()).filter_by(user=id).all()
    elif pole == 'update':
        articles = Article.query.order_by(Article.update_date.desc()).filter_by(user=id).all()
    articles = Article.query.order_by(Article.create_date.desc()).filter_by(user=id).all()
    articles_to_template = []
    for article in articles:
        if not article.remove_date:
            obj = {
                'id': article.id,
                'create_date': article.create_date,
                'update_date': article.update_date,
                'remove_date': article.remove_date,
                'user_id': article.user,
                'username': user.username,
                'title': article.title,
                'body': article.body,
                'end_date': article.end_date
            }
            articles_to_template.append(obj)
    return jsonify({'articles':articles_to_template})


@app.route('/api/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return jsonify({'Success':'User has been logouted'})


@app.route('/api/registration', methods=['POST'])
def registration():
    name = request.json['u_name']
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({'Error':'User has already registered'})

    new_user = User(name=name, username=username, password=password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'Success':'User has been registered'})

@app.route('/admin/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        
        if user:
            if not user.remove_date:
                role = Role.query.filter_by(id=user.role).first()
                if role.name == 'админ':
                    return redirect('/admin')
                else:
                    return jsonify({'error': 'user not admin'})
            else:
                return jsonify({'error':'deleted user'})
        else:
            return jsonify({'error':'Unregistered user'})

    else:
        return render_template('login.html')
