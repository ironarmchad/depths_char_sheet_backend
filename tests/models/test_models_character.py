from random import randint
from tests.conftest import random_string
from app.models.character import CharacterModel
from app.models.user import UserModel


# __init__ should create a character with an owner value
def test_init():
    owner = randint(1, 20)
    character = CharacterModel(owner)

    assert character.owner == owner


# __repr__ should return a string with owner and name
def test_repr():
    owner = randint(1, 20)
    name = random_string()
    character = CharacterModel(owner)
    character.name = name

    assert str(owner) in repr(character) and name in repr(character)


# add_character should add the character to the database
def test_add_character(app):
    with app.app_context():
        owner = UserModel('test', 'test')
        owner.add_user()
        character = CharacterModel(owner.id)

        assert not character.id

        character.add_character()

        assert character.id


# delete_character should remove character from the database
def test_delete_character(app):
    with app.app_context():
        owner = UserModel('test', 'test')
        owner.add_user()
        character = CharacterModel(owner.id)
        character.add_character()
        id = character.id

        character.delete_character()

        assert not CharacterModel.query.get(id)


# jsonify_dict should return a dictionary with id owner and name (plus more but...)
def test_jsonify_dict():
    character = CharacterModel(1)

    json = character.jsonify_dict()

    assert 'id' in json and 'owner' in json and 'name' in json


# patch_from_json should take a dict and change fields that match character fields
def test_patch_from_json(app):
    data = {
        'name': random_string(),
        'summary': random_string(),
        'char_type': random_string(),
        'game_id': randint(0, 20),
        'lore': random_string(),
        'strength': randint(0, 20),
        'reflex': randint(0, 20),
        'speed': randint(0, 20),
        'vitality': randint(0, 20),
        'awareness': randint(0, 20),
        'willpower': randint(0, 20),
        'imagination': randint(0, 20),
        'attunement': randint(0, 20),
        'faith': randint(0, 20),
        'luck': randint(0, 20),
        'charisma': randint(0, 20)
    }

    character = CharacterModel(1)
    character.patch_from_json(data)

    for key in data:
        print(key, data[key], character.__getattribute__(key))
        assert data[key] == character.__getattribute__(key)


# patch_from_json should not fail if data doesn't include all fields
def test_patch_from_json_skipping():
    data1 = {'imagination': random_string()}
    data2 = {'awareness': random_string()}

    character = CharacterModel(1)

    character.patch_from_json(data1)
    assert character.imagination == data1['imagination']

    character.patch_from_json(data2)
    assert character.awareness == data2['awareness']


# patch_from_json should not change owner
def test_patch_from_json_owner():
    owner = randint(0, 20)
    data = {
        'owner': 99
    }
    character = CharacterModel(owner)

    character.patch_from_json(data)

    assert character.owner != data['owner'] and character.owner == owner


# get_by_id should return a character using only the id
def test_get_by_id(app):
    with app.app_context():
        owner = UserModel('test', 'test')
        owner.add_user()
        character = CharacterModel(owner.id)
        character.add_character()
        id = character.id

        assert CharacterModel.get_by_id(id).owner == owner.id



