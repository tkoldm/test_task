from app import db
from app.models.dates_mixin import DateMixin
from app.models.user_model import User
from datetime import datetime


class Article(DateMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey(User.id))
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    end_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Article {self.id}>'