import os
import string
import random
import pytest

from app import create_app, db
from app.models.user import UserModel
from app.models.character import CharacterModel
from app.models.ability import AbilityModel

basedir = os.path.abspath(os.path.dirname(__file__))


def random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture
def app(request):
    app = create_app('testing')

    with app.app_context():
        db.drop_all()
        db.create_all()

    def fin():
        with app.app_context():
            db.drop_all()

    request.addfinalizer(fin)
    return app


@pytest.fixture
def populate_db(app):
    with app.app_context():
        user = UserModel('test', 'test').add_user()
        character = CharacterModel(user.id).add_character()
        ability = AbilityModel(character.id).add_ability()

        return {
            'userId': user.id,
            'characterId': character.id,
            'abilityId': ability.id
        }


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
