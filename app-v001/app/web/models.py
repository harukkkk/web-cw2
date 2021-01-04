# coding: utf-8
from . import db, flask_bcrypt, login
from flask import url_for
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)  # 用户名
    password_hash = db.Column(db.String(128))  # 密码
    register_date = db.Column(db.DateTime, default=datetime.now)  # 注册日期
    is_active = db.Column(db.Boolean, default=True)  # 用户状态
    is_superuser = db.Column(db.Boolean, default=False)  # 是否管理员用户

    def __repr__(self):
        return '<User {}>'.format(self.name)

    @property
    def password(self):
        return 'hashed password'

    @password.setter
    def password(self, pw):
        self.password_hash = flask_bcrypt.generate_password_hash(pw).decode('utf-8')

    def check_password(self, pw):
        return flask_bcrypt.check_password_hash(self.password_hash, password=pw)

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return self.is_active is True


# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))


category_article_table = db.Table(
    'association', db.Model.metadata,
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
    )


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    article_ls = db.relationship("Article", secondary=category_article_table, lazy=True)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship("User", backref=db.backref('article_ls', cascade='all, delete-orphan'), lazy=True)
    content = db.Column(db.Text)
    category_ls = db.relationship("Category", secondary=category_article_table, lazy=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)


