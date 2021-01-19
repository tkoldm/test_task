from flask_login import UserMixin
from app import db
from app.dates_mixin import DateMixin
from app.models.role_model import Role
from datetime import datetime


class User(UserMixin, DateMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    name = db.Column(db.String(128))
    role = db.Column(db.Integer, db.ForeignKey(Role.id))
    

    def __repr__(self):
        return f'<User {self.id}>'

