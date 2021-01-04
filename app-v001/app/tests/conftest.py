import pytest
import sys
sys.path.extend('..')
from web import create_app, db, models
import os


@pytest.fixture(scope='module')
def new_user():
    user = models.User(name='user001')
    user.password = 'helloFlask'
    return user


@pytest.fixture(scope='module')
def test_client():
    print('kkk- init')
    app = create_app('test')
    os.environ.setdefault('FLASK_ENV', 'test')

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def init_database(test_client):
    db.create_all()
    user1 = models.User(name='user001')
    user1.password = 'helloFlask'
    user2 = models.User(name='kennedyfamilyrecipes@gmail.com')
    user2.password = 'helloFlask'
    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()

    yield db # this is where the testing happens!

    db.drop_all()

