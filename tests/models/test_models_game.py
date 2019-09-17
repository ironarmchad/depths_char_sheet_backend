from random import randint
from tests.conftest import random_string
from app.models.game import GameModel
from app.models.user import UserModel


# __init__ should create a game
def test_init():
    st = randint(1, 20)
    game = GameModel(st)

    assert game.st_id == st


# __repr__ should return a string with name and st_id
def test_repr():
    st = randint(1, 20)
    name = random_string()
    game = GameModel(st)
    game.name = name

    assert str(st) in repr(game) and name in repr(game)


# add_game should add the game to the database
def test_add_game(app):
    with app.app_context():
        st = UserModel('test', 'test')
        st.add_user()
        game = GameModel(st.id)

        assert not game.id

        game.add_game()

        assert game.id


# jsonify_dict should return dict with 'name' and 'st_id' (plus more but...)
def test_jsonify_dict():
    game = GameModel(1)
    name = random_string()
    game.name = name

    json = game.jsonify_dict()

    assert 'name' in json and 'st_id' in json


# patch_from_json should mutate all attributes based on name
def test_patch_from_json():
    data = {
        'name': random_string(),
        'active': True,
        'lore': random_string(),
        'summary': random_string()
    }
    game = GameModel(1)

    game.patch_from_json(data)

    for key in data:
        print(key, data[key], game.__getattribute__(key))
        assert data[key] == game.__getattribute__(key)


# patch_from_json should not change st_id
def test_patch_from_json_st_id():
    data = {
        'st_id': 99
    }
    st = randint(1, 20)
    game = GameModel(st)

    assert game.st_id == st

    game.patch_from_json(data)

    assert game.st_id != data['st_id'] and game.st_id == st
