from flask import Blueprint, render_template, url_for, redirect, request, session
from flask_admin import expose
from flask_security import login_required
from app.queries import check_user_login
from app.models.user_model import User
from app.models.article_model import Article
from app.models.role_model import Role
from app.queries import check_user_registration
from app.calculate_dates import calculate_end_date
from app import app, db

def login_admin(username, role):
    session['admin_logged'] = {'is_authenticated': True,
                                'username': username,
                                'role': role}

def is_admin_logged():
    try:
        if session['admin_logged']:
            return True
        else:
            return False
    except:
        return False

def logout_admin():
    if session['admin_logged']:
        session.pop('admin_logged')

@app.route('/admin/user/edit/', methods=['POST'])
def get_edit_user():
    update_data = {}
    user_id = request.args.get('id', type=int)
    user = User.query.filter_by(id=user_id).first()
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password_hash')
    role = request.form.get('role')
    if username != user.username:
        update_data['username'] = username
    if name != user.name:
        update_data['name'] = name
    if role:
        update_data['role_id'] = role
    if update_data:
        User.query.filter_by(id=user_id).update(update_data)
    if not user.check_password(password):
        user.set_password(password)
    db.session.commit()
    return redirect('/admin/user')

@app.route('/admin/user/new/', methods=['POST'])
def add_new_user():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password_hash')
    role = request.form.get('role')
    new_user = User(name=name, username=username, role_id=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/admin/user')

@app.route('/admin/logout', methods=['POST', 'GET'])
def logout_a_user():    
    if is_admin_logged():
        logout_admin()
        return redirect('/admin')
    else:
        return redirect('/admin')


@app.route('/admin/article/edit/', methods=['POST'])
def get_edit_article():
    update_data = {}
    article_id = request.args.get('id', type=int)
    article = Article.query.filter_by(id=article_id).first()
    title = request.form.get('title')
    body = request.form.get('body')
    user_id = request.form.get('user')
    if title != article.title:
        update_data['title'] = title
    if body != article.body:
        update_data['body'] = body
    if user_id and not article.user_id:
        update_data['user_id'] = user_id
    if update_data:
        Article.query.filter_by(id=article_id).update(update_data)
    db.session.commit()
    return redirect('/admin/article')

@app.route('/admin/article/new/', methods=['POST'])
def add_new_article():
    article_id = request.args.get('id', type=int)
    title = request.form.get('title')
    body = request.form.get('body')
    user_id = request.form.get('user')
    end_date = request.form.get('end_date')

    if not end_date:
        end_date = calculate_end_date()

    new_article = Article(title=title, body=body, user_id=user_id, end_date=end_date)
    db.session.add(new_article)
    db.session.commit()
    return redirect('/admin/article')