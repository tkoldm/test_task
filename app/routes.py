# -*- coding: utf-8 -*-
from datetime import datetime
from app import app, db, login
from app.models import Role, Article, User
from flask import render_template, url_for, request, redirect, jsonify
from flask_login import current_user, login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


@app.route('/')
def index():
    return redirect(url_for('articles_list'))


@app.route('/articles')
def articles_list():
    articles = Article.query.order_by(Article.create_date.desc()).all()
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
    return jsonify({'articles': articles_to_template})


@app.route('/articles/sort_<string:pole>')
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


@app.route('/articles/<int:id>', methods=['GET','POST', 'DELETE', 'PUT'])
def article_detail(id):
    if request.method == 'GET':
        article = Article.query.get(id)
        if article.remove_date:
            return redirect(url_for('articles_list'))
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

        if current_user.is_authenticated and current_user.id == article.user and not article.remove_date:
            article = Article.query.filter_by(id = id).update({'update_date': datetime.utcnow()})
            db.session.commit()
            return redirect(url_for('articles_list'))
        else:
            return jsonify({'Error':'Article deleted'})
    
    else:
        try:
            article = Article.query.get(id)
        except:
            return jsonify({'Error':'Article doesn\'t exist'})
            
        if current_user.is_authenticated and current_user.id == article.user and not article.remove_date:
            article = Article.query.filter_by(id = id).update({'remove_date': datetime.utcnow()})
            db.session.commit()
            return redirect(url_for('articles_list'))
        else:
            return jsonify({'Error':'Article deleted'})


@app.route('/add_article', methods=['POST'])
def add_new_article():
    if current_user.is_authenticated:
        title = request.form['title']
        body = request.form['body']

        article = Article(title=title, body=body, user=current_user.id)

        db.session.add(article)
        db.session.commit()
        return redirect(url_for('articles_list'))

    else:
        return redirect(url_for('authorization'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/authorization', methods=['POST'])
def authorization():
    if current_user.is_authenticated:
        return redirect(url_for('articles_list'))
        
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
        
    if not user.block_date:
        if user:
            login_user(user)
            return redirect(f'/profile/{user.id}')
    else:
        return redirect(url_for('articles_list'))


@app.route('/profile/<int:id>')
def user_profile(id):
    user = User.query.filter_by(id=id).first_or_404()
    articles = Article.query.order_by(Article.create_date.desc()).filter_by(user=id).all()
    articles_to_template = []
    for article in articles:
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


@app.route('/profile/<int:id>/sort_<string:pole>')
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


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('articles_list'))


@app.route('/registration', methods=['POST'])
def registration():
    name = request.form['u_name']
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user:
        return redirect(url_for('authorization'))

    new_user = User(name=name, username=username, password=password)

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('articles_list'))
