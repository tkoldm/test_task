from flask import redirect, url_for, render_template
from flask_login import current_user
#from flask_admin import AdminIndexView, expose
from flask_admin.model import BaseModelView
from flask_admin.contrib.sqla import ModelView
from app import db
from app import admin_routes
from app.user_model import User
from app.role_model import Role

class AdminView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated:
            role_id = current_user.role
            role = Role.query.filter_by(id=role_id).first()
            if role.name != 'user':
                if role.name == 'moderator':
                    can_create = False
                    can_delete = False
                    can_edit = False
                return True
        return False