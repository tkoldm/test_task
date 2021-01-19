from flask import render_template, url_for, request
from flask_admin import expose
from flask_login import current_user, login_user, logout_user
from app.user_model import User
from app.role_model import Role
from app import app, db

@app.route('/login', methods=['POST', 'GET'])
def login_admin_panel():
    if current_user.is_authenticated:
        return 'Already auth'
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            if user.password == password:
                if not user.remove_date:
                    login_user(user)
                    return 'Loged in'
                else:
                    return 'User removed'
            else:
                return 'Wrong password'
        else:
            return 'Incorrect username'
                    
@app.route('/logout', methods=['POST', 'GET'])
def logout_a_user():    
        if current_user.is_authenticated:
            logout_user()
            return 'Logouted'
        else:
            return 'Not auth'

@expose('/admin_view', methods=['POST', 'GET'])
def admin_view():
    pass