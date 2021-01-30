from flask import Blueprint, render_template, url_for, redirect, request, session
from app.models.user_model import User
from app.models.role_model import Role
from app import app, db

admin_blueprint = Blueprint('admin_blueprint', __name__, template_folder='templates')

def login_admin():
    session['admin_logged'] = 1

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


@admin_blueprint.route('/login', methods=['POST', 'GET'])
def login_admin_panel():
    if is_admin_logged():
        return redirect('/admin/')
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).filter_by(is_admin=True).filter_by(remove_date=None).first()
        if user and user.check_password(password):
            login_admin()
            return redirect('/admin/user')            
        else:
            return redirect('/admin')
                    
@admin_blueprint.route('/user/edit/', methods=['POST'])
def get_edit():
    user_id = request.args.get('id', type=int)
    user = User.query.filter_by(id=user_id).first()
    password = request.form.get('password_hash')
    if not user.check_password(password):
        user.set_password(password)
        db.session.commit()
    return redirect('/admin/user')

@admin_blueprint.route('/logout', methods=['POST', 'GET'])
def logout_a_user():    
    if is_admin_logged():
        logout_admin()
        return redirect('/admin')
    else:
        return redirect('/admin')
