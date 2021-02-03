from flask import Blueprint, render_template, url_for, redirect, request, session
from flask_admin import expose
from flask_security import login_required
from app.queries import check_user_login
from app.models.user_model import User
from app.models.role_model import Role
from app import app, db

def login_admin(username):
    session['admin_logged'] = {'is_authenticated': True,
                                'username': username}

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
def get_edit():
    user_id = request.args.get('id', type=int)
    user = User.query.filter_by(id=user_id).first()
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password_hash')
    update_data = {'username': username, 'name':name, 'is_admin':True}
    if request.form.get('is_admin'):
        update_data['is_admin'] = True
    User.query.filter_by(id=user_id).update(update_data)
    if not user.check_password(password):
        user.set_password(password)
        db.session.commit()
    return redirect('/admin/user')

@app.route('/admin/user/new/', methods=['POST'])
def add_new():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password_hash')
    if request.form.get('is_admin'):
        new_user = User(name=name, username=username, is_admin=True)
    else:
        new_user = User(name=name, username=username)
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
