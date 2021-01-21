from flask_login import UserMixin
from app import db
from app.models.dates_mixin import DateMixin
from app.models.role_model import Role

class User(UserMixin, DateMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    name = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    

    def __repr__(self):
        return f'<User {self.id}>'

