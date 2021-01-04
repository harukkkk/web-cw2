# coding: utf-8
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """配置基类"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'should-be-changed-to-a-strong-secret')
    DEBUG = False
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = SECRET_KEY


class DevelopmentConfig(Config):
    """开发时使用的数据库"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """测试时使用的数据库"""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'test.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """上线时使用MySql数据库"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{db_host}:{port}/{database}?charset=utf8mb4'.format(
        user='root',
        password='mayulong622',
        db_host='127.0.0.1',
        port='3306',
        database='todo_list',
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False



