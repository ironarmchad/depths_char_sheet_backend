from random import randint

from tests.conftest import random_string
from app.models.user import UserModel
from app.models.character import CharacterModel
from app.models.ability import AbilityModel


# get request to /ability/get/<id> should return an ability
def test_ability_get(auth, populate_db):
    auth.login('test', 'test')
    response = auth.get(f'/ability/get/{populate_db["abilityId"]}')
    json = response.get_json()

    assert response.status_code == 200
    assert 'id' in json and 'charId' in json


# get request to /ability/get/<id> with bad id should return 400
def test_ability_get_bad_id(auth, populate_db):
    auth.login('test', 'test')
    response = auth.get(f'/ability/get/-1')

    assert response.status_code == 400


# get request to /ability/get/<id> should return 400 if
def test_ability_get_wrong_ownder(app, auth, populate_db):
    with app.app_context():
        UserModel('silly', 'bugger').add_user()

    auth.login('silly', 'bugger')
    response = auth.get(f'/ability/get/{populate_db["abilityId"]}')

    assert response.status_code == 400


# patch request to /ability/get/<id> should mutate ability
def test_ability_patch(app, auth, populate_db):
    new_name = random_string(7)
    with app.app_context():
        assert not AbilityModel.get_by_id(populate_db['abilityId']).name

    auth.login('test', 'test')
    auth.patch(f'/ability/get/{populate_db["abilityId"]}', {'ability': {'name': new_name}})

    with app.app_context():
        assert AbilityModel.get_by_id(populate_db['abilityId']).name == new_name


# patch request to /ability/get/<id> should return 400 if provided with a bad id
def test_ability_patch_bad_id(app, auth, populate_db):
    auth.login('test', 'test')
    response = auth.patch(f'/ability/get/-1', {'ability': {'name': 'silly'}})

    assert response.status_code == 400


# delete request to /ability/get/<id> should remove ability from database
def test_ability_delete(app, auth, populate_db):
    with app.app_context():
        assert AbilityModel.get_by_id(populate_db['abilityId'])

    auth.login('test', 'test')
    auth.delete(f'/ability/get/{populate_db["abilityId"]}')

    with app.app_context():
        assert not AbilityModel.get_by_id(populate_db['abilityId'])


# delete request to /ability/get/<id> should return 400 if provided with bad id
def test_ability_delete_bad_id(app, auth, populate_db):
    auth.login('test', 'test')
    response = auth.delete(f'/ability/get/-1')

    assert response.status_code == 400


# post request to /ability/new/<char_id> should make a new ability
def test_ability_new_post(app, auth, populate_db):
    new_name = random_string(7)
    auth.login('test', 'test')
    response = auth.post(f'/ability/new/{populate_db["characterId"]}', {'name': new_name})

    assert response.status_code == 200
    with app.app_context():
        assert AbilityModel.get_by_id(response.get_json()['id'])


# post request to /ability/new/<char_id> should return 400 if you attempt to add ability to a character you don't own
def test_ability_new_post_bad_request(app, auth, populate_db):
    with app.app_context():
        UserModel('silly', 'bugger').add_user()

    auth.login('silly', 'bugger')
    response = auth.post(f'/ability/new/{populate_db["characterId"]}', {'ability': {'name': 'silly'}})

    assert response.status_code == 400


# get request to /ability/all/<char_id> should return a list of abilities
def test_ability_all_get(app, auth, populate_db):
    total_abilities = randint(1, 20)
    with app.app_context():
        char = CharacterModel(populate_db['userId']).add_character()
        for i in range(0, total_abilities):
            AbilityModel(char.id).add_ability()

        auth.login('test', 'test')
        response = auth.get(f'/ability/all/{char.id}')

        assert response.status_code == 200
        assert len(response.get_json()['abilities']) == total_abilities


# get request to /ability/all/<char_id> should return 400 if trying to access abilities that don't belong to user
def test_ability_all_get_bad_request(app, auth, populate_db):
    with app.app_context():
        UserModel('silly', 'bugger').add_user()

    auth.login('silly', 'bugger')
    response = auth.get(f'/ability/all/{populate_db["characterId"]}')

    assert response.status_code == 400
