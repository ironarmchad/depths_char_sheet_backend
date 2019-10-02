from random import randint

from tests.conftest import random_string
from app.models.ability import AbilityModel
from app.models.character import CharacterModel


# __init__ should create an ability with a character id value
def test_init():
    char_id = randint(1, 100)
    ability = AbilityModel(char_id)

    assert ability.charId == char_id


# __repr__ should return string with id, charId and name
def test_repr(app, populate_db):
    char_id = populate_db['characterId']
    with app.app_context():
        ability = AbilityModel(char_id)
        ability.name = random_string(7)
        ability.add_ability()

        assert str(char_id) in repr(ability)
        assert str(ability.id) in repr(ability)
        assert str(ability.name) in repr(ability)


# add_ability should add the ability to the database
def test_add_ability(app, populate_db):
    with app.app_context():
        char_id = populate_db['characterId']
        ability = AbilityModel(char_id)

        assert not ability.id

        ability.add_ability()

        assert ability.id


# delete_ability should remove the ability from the database
def test_delete_ability(app, populate_db):
    with app.app_context():
        ability = AbilityModel(populate_db['characterId']).add_ability()

        assert AbilityModel.query.get(ability.id)

        ability.delete_ability()

        assert not AbilityModel.query.get(ability.id)


# jsonify_dict should return a dictionary with at least id and char_id
def test_jsonify_dict(app, populate_db):
    with app.app_context():
        ability = AbilityModel(populate_db['characterId']).add_ability()

        assert 'id' in ability.jsonify_dict()
        assert 'charId' in ability.jsonify_dict()


# patch_from_json should faithfully change all fields but id and charId
def test_patch_from_json(app, populate_db):
    json = {
        'name': random_string(7),
        'type': random_string(4),
        'summary': random_string(50),
        'lore': random_string(200),
        'macro': random_string(20)
    }
    with app.app_context():
        ability = AbilityModel(populate_db['characterId'])
        ability.patch_from_json(json)
        ability.add_ability()

        for key in json:
            assert json[key] == getattr(ability, key)


# test_patch_from_json should not change id or charId
def test_patch_from_json_skipping(app, populate_db):
    json = {
        'id': -1,
        'charId': -1
    }
    with app.app_context():
        ability = AbilityModel(populate_db['characterId'])

        ability.patch_from_json(json)
        ability.add_ability()

        assert ability.id != -1
        assert ability.charId != -1


# get_by_id should retrieve an ability by its id
def test_get_by_id(app, populate_db):
    with app.app_context():
        ability = AbilityModel(populate_db['characterId']).add_ability()

        assert AbilityModel.get_by_id(ability.id)


# get_by_char_id should retrieve a list of abilitys with a char_id provided
def test_get_by_char_id(app, populate_db):
    with app.app_context():
        char = CharacterModel(populate_db['userId']).add_character()
        for i in range(0, 5):
            AbilityModel(char.id).add_ability()

        assert len(AbilityModel.get_by_char_id(char.id)) == 5


