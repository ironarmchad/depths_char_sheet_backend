import os
import pytest

from app import create_app, db
from app.models.user import UserModel
from app.models.character import CharacterModel
from app.models.game import GameModel

basedir = os.path.abspath(os.path.dirname(__file__))



@pytest.fixture
def app(request):
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:PIANO@230jap@localhost/testing'
    })

    with app.app_context():
        db.drop_all()
        db.create_all()
        UserModel('test', 'test')
        userId = UserModel.find_by_username('test').id
        CharacterModel(userId)
        GameModel(userId)

    def fin():
        with app.app_context():
            db.drop_all()

    request.addfinalizer(fin)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/user/login',
            data={'username': username, 'password': password}
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)
