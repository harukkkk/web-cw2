# coding: utf-8
import pytest
from web.models import User
from web import db


def test_new_user(test_client, init_database):
    user = User(name='user004')
    user.password = 'helloWorld'
    db.session.add(user)
    db.session.commit()
    assert user.password_hash != 'helloWorld'
    assert user.is_active is True
    assert user.is_superuser is False
    assert User.query.filter(User.name == 'user004').first() is not None


