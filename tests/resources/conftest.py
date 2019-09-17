import pytest
import json

from app.models.user import UserModel
from app.models.character import CharacterModel


@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client
        self.accessToken = ''

    def login(self, username='test1', password='test'):
        jwt = self._client.post(
            '/user/login',
            data=json.dumps({'username': username, 'password': password}),
            content_type='application/json'
        )

        self.accessToken = jwt.get_json()['accessToken']
        return jwt

    def get(self, location):
        return self._client.get(
            location,
            headers={'Authorization': 'Bearer ' + self.accessToken},
        )

    def post(self, location, content):
        return self._client.post(
            location,
            headers={'Authorization': 'Bearer ' + self.accessToken},
            content_type='application/json',
            data=json.dumps(content)
        )

    def patch(self, location, content):
        return self._client.patch(
            location,
            headers={'Authorization': 'Bearer ' + self.accessToken},
            content_type='application/json',
            data=json.dumps(content)
        )

    def delete(self, location):
        return self._client.delete(
            location,
            headers={'Authorization': 'Bearer ' + self.accessToken}
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def populate_db(app):
    with app.app_context():
        user1 = UserModel('test1', 'test').add_user()
        user2 = UserModel('test2', 'test').add_user()
        user3 = UserModel('test3', 'test').add_user()

        character1 = CharacterModel(user1.id).add_character()

