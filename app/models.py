from flask_login import UserMixin
from app import db
from datetime import datetime


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)


    def __repr__(self):
        return f'<Role {self.id}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    name = db.Column(db.String(128))
    block_date = db.Column(db.DateTime)
    role = db.Column(db.Integer, db.ForeignKey(Role.id))
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return f'<User {self.id}>'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    remove_date = db.Column(db.DateTime)
    user = db.Column(db.Integer, db.ForeignKey(User.id))
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    end_date = db.Column(db.DateTime)


    def __repr__(self):
        return f'<Article {self.id}>'