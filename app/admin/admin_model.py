from flask import redirect, url_for, render_template
from flask_login import current_user
from flask_admin.model import BaseModelView
from flask_admin.contrib.sqla import ModelView
from app import db
from app.admin import admin_routes
from app.models.user_model import User
from app.models.role_model import Role

class AdminView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return True
        return False