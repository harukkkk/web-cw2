# coding: utf-8
from flask import Blueprint, current_app
from werkzeug.local import LocalProxy
root_blueprint = Blueprint('main', __name__, template_folder='templates')
logger = LocalProxy(lambda: current_app.logger)
from . import db
import os
from flask import (
    render_template, flash, redirect, url_for, request,
    abort, jsonify,
    )
from werkzeug.urls import url_parse
from .forms import LoginForm, RegisterForm, ArticleCreateForm
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Category, Article
import base64
import binascii


@root_blueprint.route('/test')
def first():
    return render_template('test.html', title='Test')


@root_blueprint.route('/', methods=['get'])
def index():
    q = request.args.get('q', '').strip()
    query = Article.query.order_by(Article.created_at.desc())
    if q:
        query = query.filter(Article.title.ilike(f'%{q}%'))
    ls = query.all()
    if q:
        title = 'Search Results'
    else:
        title = 'All Articles'
    return render_template('index.html', title=title, ls=ls)


@root_blueprint.route('/login/', methods=['get', 'post'])
def login():
    """User Login View"""
    # print(dir(root_blueprint))
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '' or next_page.startswith('/logout'):
        next_page = url_for('main.index')
    if current_user.is_authenticated:
        return redirect(next_page)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None:
            flash('Username or Password Wrong', category='danger')
        else:
            if not user.check_password(form.password.data):
                flash('Username or Password Wrong', category='danger')
            else:
                flash('Welcome back', category='success')
                login_user(user, remember=form.remember_me.data)
                logger.info('%s have signed in with IP %s' % (user.name, request.remote_addr))
                return redirect(next_page)

    return render_template('login.html', title='User Login', form=form)


@root_blueprint.route('/logout/')
@login_required
def logout():
    """User Logout"""
    logout_user()
    return redirect(url_for('main.login'))


@root_blueprint.route('/register/', methods=['post', 'get'])
def register():
    """User Register"""

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(name=form.username.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        logger.info('%s have registered in IP %s' % (user.name, request.remote_addr))
        flash('Your Account Created, PLease Login', category='success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='User Register', form=form)


@root_blueprint.route('/category/list')
def category_ls():
    data = []
    for cat in Category.query.order_by(Category.id.desc()).all():
        data.append({
            'id': cat.id,
            'name': cat.name
            })
    return jsonify(status='success', data=data)


@root_blueprint.route('/category/create/<string:name>')
@login_required
def category_create(name):
    name = base64.urlsafe_b64decode(name).decode().strip()
    if len(name) > 128 or len(name) < 3:
        abort(500)
    cat = Category.query.filter(Category.name == name).first()
    if isinstance(cat, Category):
        return jsonify(flag=False, name=name, id=cat.id)
    cat = Category(name=name)
    db.session.add(cat)
    db.session.commit()
    logger.info('%s have created category %s in with IP %s' % (current_user.name, cat.name, request.remote_addr))
    return jsonify(flag=True, name=name, id=cat.id)


@root_blueprint.route('/article/create', methods=['get', 'post'])
@login_required
def article_create():
    if request.method == 'POST':
        is_submitted = True
        form = ArticleCreateForm(data=request.data)
        form.categories.choices = [(cat.id, cat.name) for cat in
                                   Category.query.order_by(Category.id.desc()).all()]  # + [(1, 'hello'), (2, 'tttt')]
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            category_id_ls = form.categories.data
            article = Article(title=title, content=content, user_id=current_user.id)
            db.session.add(article)
            db.session.commit()
            ls = []

            for i in category_id_ls:
                cat = Category.query.filter(Category.id == i).first()
                if cat:
                    ls.append(cat)

            article.category_ls = ls
            db.session.add(article)
            db.session.commit()
            logger.info(
                '%s have created article %s in with IP %s' % (current_user.name, article.title, request.remote_addr))
            return redirect(url_for('main.article_view', article_id=article.id, article_title=article.title))
    else:
        form = ArticleCreateForm()
        form.categories.choices = [(cat.id, cat.name) for cat in
                                   Category.query.order_by(Category.id.desc()).all()]  # + [(1, 'hello'), (2, 'tttt')]
        is_submitted = False

    return render_template('article_create.html', title='Create Article', form=form, is_submitted=is_submitted)


@root_blueprint.route('/article/my')
@login_required
def article_my():
    query = Article.query.order_by(Article.created_at.desc()).filter(Article.user_id==current_user.id)
    ls = query.all()
    title = 'My Articles'
    return render_template('index.html', title=title, ls=ls)


@root_blueprint.route('/article/view/<int:article_id>/<string:article_title>')
@root_blueprint.route('/article/view/<int:article_id>')
def article_view(article_id, article_title=None):
    article = Article.query.filter(Article.id == article_id).first_or_404()
    return render_template('article_view.html', title=f'{article.title} - View Article',
                           article=article)


@root_blueprint.route('/article/edit/<int:article_id>', methods=['get', 'post'])
@login_required
def article_edit(article_id):

    article = Article.query.order_by(Article.created_at.desc()).\
        filter(Article.user_id == current_user.id).\
        filter(Article.id == article_id).first_or_404()

    if request.method == 'POST':
        is_submitted = True
        form = ArticleCreateForm(data=request.data, obj=article)
        form.categories.choices = [(cat.id, cat.name) for cat in
                                   Category.query.order_by(Category.id.desc()).all()]  # + [(1, 'hello'), (2, 'tttt')]
        # form.categories.data = [cat.id for cat in article.category_ls]

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            category_id_ls = form.categories.data
            article = Article(title=title, content=content, user_id=current_user.id)
            db.session.add(article)
            db.session.commit()
            ls = []

            for i in category_id_ls:
                cat = Category.query.filter(Category.id == i).first()
                if cat:
                    ls.append(cat)

            article.category_ls = ls
            db.session.add(article)
            db.session.commit()
            logger.info(
                '%s have updated article %s in with IP %s' % (current_user.name, article.title, request.remote_addr))
            return redirect(url_for('main.article_view', article_id=article.id, article_title=article.title))
    else:
        form = ArticleCreateForm(obj=article)
        form.categories.choices = [(cat.id, cat.name) for cat in
                                   Category.query.order_by(Category.id.desc()).all()]  # + [(1, 'hello'), (2, 'tttt')]
        form.categories.data = [cat.id for cat in article.category_ls]
        is_submitted = False

    return render_template('article_create.html', title='Update Article', form=form, is_submitted=is_submitted)


@root_blueprint.route('/article/delete/<int:article_id>', methods=['get'])
@login_required
def article_delete(article_id):
    article = Article.query.order_by(Article.created_at.desc()).\
        filter(Article.user_id == current_user.id).\
        filter(Article.id == article_id).first_or_404()
    logger.info(
        '%s have deleted article %s in with IP %s' % (current_user.name, article.title, request.remote_addr))
    db.session.delete(article)
    db.session.commit()
    flash(message='Your article deleted', category='success')
    return redirect(url_for('main.article_my'))
