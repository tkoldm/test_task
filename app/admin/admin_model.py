from flask import redirect, url_for, render_template, session, request
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app import db
from app.models.user_model import User
from app.models.role_model import Role
from app.admin.admin_routes import is_admin_logged, login_admin

class IndexView(AdminIndexView):
    @expose('/', methods=['POST', 'GET'])
    def index(self):
        if request.method == 'GET':
            user = None
            if is_admin_logged():
                user = session['admin_logged']
            return self.render('admin/index.html', user=user)
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).filter_by(is_admin=True).filter_by(remove_date=None).first()
            if user and user.check_password(password):
                login_admin(user.username)
            return redirect('/admin/')

class AdminView(ModelView):

    column_exclude_list = ['password_hash', ]


    def is_accessible(self):
        try:
            if session['admin_logged']:
                return True
        except:
            return False