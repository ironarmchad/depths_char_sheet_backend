import os
import string
import random
import pytest

from app import create_app, db

basedir = os.path.abspath(os.path.dirname(__file__))


def random_string(length = 10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture
def app(request):
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:PIANO@230jap@localhost/testing'
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

    def fin():
        with app.app_context():
            db.drop_all()

    request.addfinalizer(fin)
    return app




@pytest.fixture
def runner(app):
    return app.test_cli_runner()


