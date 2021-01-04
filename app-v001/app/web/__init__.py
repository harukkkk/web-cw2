# coding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
import logging
import config

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
login = LoginManager()
login.login_view = 'main.login'


def create_app(env_name: str = None):
    if env_name is None:
        env_name = os.environ.get('FLASK_ENV', 'development')
    app = Flask(__name__)
    if env_name == 'production':
        app.config.from_object(config.ProductionConfig)
    elif env_name == 'test':
        app.config.from_object(config.TestConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    db.init_app(app)
    flask_bcrypt.init_app(app)
    CSRFProtect(app)
    login.init_app(app)

    from .models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    # logging
    handler = logging.FileHandler('running.log', encoding='UTF-8')
    error_log = logging.FileHandler('error.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    error_log.setLevel(logging.ERROR)
    logging_format = logging.Formatter('%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s')
    testing_format = logging.Formatter(
        '%(asctime)s - %(pathname)s\\%(funcName)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    handler.setFormatter(logging_format)
    error_log.setFormatter(testing_format)

    app.logger.addHandler(handler)
    app.logger.addHandler(error_log)


def register_blueprints(app):
    from .routes import root_blueprint

    app.register_blueprint(root_blueprint)








