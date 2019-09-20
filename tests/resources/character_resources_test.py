import json

from app.models.user import UserModel
from app.models.character import CharacterModel


# post to /character/new should return a character id and store a character in the database
def test_character_new_post(app, auth, populate_db):
    auth.login('test1', 'test')
    response = auth.post('/character/new', {'name': 'test'})

    assert response.status_code == 200
    with app.app_context():
        assert CharacterModel.get_by_id(response.get_json()['id'])


# get to /character/<char_id> should return json with minimum of id and owner
def test_character_get(auth, populate_db):
    auth.login('test1', 'test')
    response = auth.get('/character/get/1')
    json = response.get_json()

    print(json)
    assert response.status_code == 200
    assert 'id' in json and 'owner' in json


# get request to /character/<char_id> should return 400 if identity doesn't match
def test_character_get_wrong_owner(auth, populate_db):
    auth.login('test2', 'test')
    response = auth.get('/character/get/1')

    assert response.status_code == 400


# get request to /character/<char_id> should return 400 if no character exists
def test_character_get_no_character(app, auth):
    # have to make a user to login rather than populate_db so that there aren't characters
    with app.app_context():
        user = UserModel('test', 'test').add_user()
    auth.login('test', 'test')
    response = auth.get('/character/get/1')

    assert response.status_code == 400


# patch request to /character/get/<char_id> should mutate character
def test_character_patch(app, auth, populate_db):
    with app.app_context():
        assert not CharacterModel.get_by_id(1).name

    auth.login('test1', 'test')
    auth.patch('/character/get/1', {'name': 'silly'})

    with app.app_context():
        assert CharacterModel.get_by_id(1).name == 'silly'


# patch request to /character/get/<char_id> should throw 400 if wrong owner sends request
def test_character_patch_bad_request(client, auth, populate_db):
    auth.login('test2', 'test')

    response = auth.patch('/character/get/1', {'name': 'silly'})

    assert response.status_code == 400


# delete request to /character/get/<char_id> should delete the db entry
def test_character_delete(app, auth, populate_db):
    with app.app_context():
        assert CharacterModel.get_by_id(1)

    auth.login('test1', 'test')
    auth.delete('/character/get/1')

    with app.app_context():
        assert not CharacterModel.get_by_id(1)


# delete request to /character/get/<char_id> should return 400 if user isn't owner
def test_character_delete_bad_request(auth, populate_db):
    auth.login('test2', 'test')

    response = auth.delete('/character/get/1')

    assert response.status_code == 400


# get request to /character/all should return list of characters
def test_character_all_get(auth, populate_db):
    auth.login('test1', 'test')

    response = auth.get('/character/all')

    assert response.status_code == 200
    assert 'characters' in response.get_json()
    assert len(response.get_json()['characters']) > 0


# get request to /character/all should return 400 if no characters
def test_character_all_get_no_characters(auth, populate_db):
    auth.login('test2', 'test')

    response = auth.get('/character/all')

    assert response.status_code == 400
