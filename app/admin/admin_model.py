from flask import redirect, url_for, render_template, session, request
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app import db, logger
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
            user = User.query.filter_by(username=username).filter_by(remove_date=None).first()
            role = Role.query.filter_by(id=user.role_id).first()
            if user and user.check_password(password) and (role.name == 'admin' or role.name == 'moderator'):
                login_admin(user.username, role.name)
                logger.info(f"user:{role.name} {username} - is authenticated in admin panel")
            return redirect('/admin/')

class AdminView(ModelView):
    
    column_exclude_list = ['password_hash', ]

    def is_accessible(self):
        try:
            if session['admin_logged']:
                if session['admin_logged'].get('role') == 'moderator':
                    self.can_create = False
                    self.can_delete = False
                    self.can_edit = False
                    self.can_export = False
                elif session['admin_logged'].get('role') == 'admin':
                    self.can_create = True
                    self.can_delete = True
                    self.can_edit = True
                    self.can_export = True
                return True
        except:
            return False