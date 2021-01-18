# -*- coding: utf-8 -*-
from datetime import datetime
from flask import g, url_for, request, redirect, jsonify
from flask_login import current_user
from app.auth import basic_auth
from app import app, db
from config import ARTICLES_PER_PAGE
from app.article_model import Article
from app.user_model import User
from app.errors import error_response

@app.route('/')
def index():
    return redirect(url_for('articles_list'))


@app.route('/api/articles')
def articles_list():

    page = request.args.get('page', 1, type=int)
    sort_type = request.args.get('sort_by', 'date', type=str)

    if sort_type == 'date':
        articles = Article.query.order_by(Article.create_date.desc()).paginate(page, ARTICLES_PER_PAGE, False)
    elif  sort_type== 'title':
        articles = Article.query.order_by(Article.title.desc()).paginate(page, ARTICLES_PER_PAGE, False)
    elif sort_type == 'update':
        articles = Article.query.order_by(Article.update_date.desc()).paginate(page, ARTICLES_PER_PAGE, False)
    elif sort_type == 'user':
        articles = Article.query.order_by(Article.user.desc()).paginate(page, ARTICLES_PER_PAGE, False)
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


@app.route('/api/articles/<int:id>', methods=['GET'])
def article_detail(id):
    article = Article.query.get(id)
    if article.remove_date:
        return error_response(410, 'Article has been deleted')
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
    

@app.route('/api/articles/<int:id>', methods=['DELETE', 'PUT'])
@basic_auth.login_required
def article_detail_ch(id):
    if request.method == 'PUT':
        
        if g.current_user.is_authenticated:
            try:
                article = Article.query.get(id)
            except:
                return error_response(404, 'Article doesn\'t exist')

            if not g.current_user.remove_date:
                if g.current_user.id == article.user:
                    if not article.remove_date:
                        article = Article.query.filter_by(id = id).update({'update_date': datetime.utcnow()})
                        db.session.commit()
                        return jsonify({'Success':'Article has been updated'})
                    else:
                        return error_response(410, 'Article deleted')
                else:
                    return error_response(403, 'Atricle from another user')
            else:
                return error_response(410, 'Deleted user')
        else:
            return error_response(401)

    else:
        if g.current_user.is_authenticated:
            try:
                article = Article.query.get(id)
            except:
                return error_response(404, 'Article doesn\'t exist')

            if not g.current_user.remove_date:
                if user_id == article.user:
                    if not article.remove_date:
                        article = Article.query.filter_by(id = id).update({'remove_date': datetime.utcnow()})
                        db.session.commit()
                        return jsonify({'Success':'Article deleted'})
                    else:
                        return error_response(410, 'Article deleted')
                else:
                    return error_response(403, 'Atricle from another user')
            else:
                return error_response(410, 'Deleted user')
        else:
            return error_response(401)


@app.route('/api/add_article', methods=['POST'])
@basic_auth.login_required
def add_new_article():
    if g.current_user.is_authenticated:
        if not request.json:
            return error_response(400, 'Incorrect type')

        if not g.current_user.remove_date:
            title = request.json['title']
            body = request.json['body']                
            article = Article(title=title, body=body, user=g.current_user.id)                
            db.session.add(article)
            db.session.commit()            
            return jsonify({'Success':'Artlicle has been added'})
        else:
            return error_response(401, f'User {user.username} has been blocked')
    else:
        return error_response(401)
