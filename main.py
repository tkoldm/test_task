# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user

app = Flask(__name__)

app.secret_key = 'AAA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    name = db.Column(db.String(128))
    block_date = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)
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


@app.route('/')
def index():
    return redirect(url_for('articles_list'))


@app.route('/articles')
def articles_list():
    articles = Article.query.order_by(Article.create_date.desc()).all()
    articles_to_template = []
    for article in articles:
        if not article.remove_date:
            user = User.query.filter_by(id=article.user).first()
            obj = {
                'id': article.id,
                'create_date': article.create_date,
                'update_date': article.update_date,
                'remove_date': article.remove_date,
                'user_id': article.user,
                'username': user.username,
                'title': article.title,
                'body': article.body,
                'end_date': article.end_date
            }
            articles_to_template.append(obj)
    return render_template('articles.html', title='Объявления', articles=articles_to_template)


@app.route('/articles/sort_<string:pole>')
def article_sort(pole):
    if pole == 'title':
        articles = Article.query.order_by(Article.title.desc()).all()
    elif pole == 'update':
        articles = Article.query.order_by(Article.update_date.desc()).all()
    elif pole == 'user':
        articles = Article.query.order_by(Article.user.desc()).all()
    articles_to_template = []
    for article in articles:
        if not article.remove_date:
            user = User.query.filter_by(id=article.user).first()
            obj = {
                'id': article.id,
                'create_date': article.create_date,
                'update_date': article.update_date,
                'remove_date': article.remove_date,
                'user_id': article.user,
                'username': user.username,
                'title': article.title,
                'body': article.body,
                'end_date': article.end_date
            }
            articles_to_template.append(obj)
    return render_template('articles.html', title='Объявления', articles=articles_to_template)


@app.route('/articles/<int:id>')
def article_detail(id):
    article = Article.query.get(id)
    if article.remove_date:
        return redirect(url_for('articles_list'))
    user = User.query.get(article.user)
    print(article.id)
    return render_template('article_detail.html', title='Объявления', article=article, username=user.username)


@app.route('/add_article', methods=['POST', 'GET'])
def add_new_article():
    if current_user.is_authenticated:
        if request.method == "POST":
            title = request.form['title']
            body = request.form['body']

            article = Article(title=title, body=body, user=current_user.id)

            try:
                db.session.add(article)
                db.session.commit()
                return redirect(url_for('articles_list'))
            except:
                return 'Error'


        else:
            return render_template('add_article.html')
    else:
        return redirect(url_for('authorization'))


@app.route('/articles/<int:id>/update')
def update_article(id):
    if current_user.is_authenticated:
        
        article = Article.query.filter_by(id = id).update({'update_date': datetime.utcnow()})
        if not article.remove_date:
            db.session.commit()
        return redirect(url_for('articles_list'))

    else:
        return redirect(url_for('articles_list'))


@app.route('/articles/<int:id>/delete')
def delete_article(id):
    if current_user.is_authenticated:
        article = Article.query.get_or_404(id)
        
        if not article.remove_date:
            article = Article.query.filter_by(id = id).update({'remove_date': datetime.utcnow()})
            db.session.commit()
            return redirect(url_for('articles_list'))
    else:
        return redirect(url_for('articles_list'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/authorization', methods=['POST', 'GET'])
def authorization():
    if current_user.is_authenticated:
        return redirect(url_for('articles_list'))

    if request.method == "POST":
        
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        
        if not user.block_date:
            if user:
                login_user(user)
                return redirect(f'/profile/{user.id}')
        else:
            return redirect(url_for('articles_list'))

    else:
        return render_template('authorization.html')


@app.route('/profile/<int:id>')
def user_profile(id):
    user = User.query.filter_by(id=id).first_or_404()
    articles = Article.query.order_by(Article.create_date.desc()).filter_by(user=id).all()
    articles_to_template = []
    for article in articles:
        if not article.remove_date:
            obj = {
                'id': article.id,
                'create_date': article.create_date,
                'update_date': article.update_date,
                'remove_date': article.remove_date,
                'user': article.user,
                'title': article.title,
                'body': article.body,
                'end_date': article.end_date
            }
            articles_to_template.append(obj)
    if current_user.is_authenticated and current_user.id == id:
        return render_template('user_profile.html', articles=articles_to_template, user=user.name)
    else:
        return render_template('profile.html', articles=articles_to_template, user=user.name)


@app.route('/profile/<int:id>/sort_<string:pole>')
def user_profile_sort(id, pole):
    user = User.query.filter_by(id=id).first_or_404()
    if pole == 'title':
        articles = Article.query.order_by(Article.title.desc()).filter_by(user=id).all()
    elif pole == 'update':
        articles = Article.query.order_by(Article.update_date.desc()).filter_by(user=id).all()
    articles = Article.query.order_by(Article.create_date.desc()).filter_by(user=id).all()
    articles_to_template = []
    for article in articles:
        if not article.remove_date:
            obj = {
                'id': article.id,
                'create_date': article.create_date,
                'update_date': article.update_date,
                'remove_date': article.remove_date,
                'user': article.user,
                'title': article.title,
                'body': article.body,
                'end_date': article.end_date
            }
            articles_to_template.append(obj)
    if current_user.is_authenticated and current_user.id == id:
        return render_template('user_profile.html', articles=articles_to_template, user=user.name)
    else:
        return render_template('profile.html', articles=articles_to_template, user=user.name)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('articles_list'))


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        name = request.form['u_name']
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            return redirect(url_for('authorization'))

        new_user = User(name=name, username=username, password=password)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('articles_list'))
    else:
        return render_template('registration.html')


if __name__ == '__main__':
    app.run(debug=True)