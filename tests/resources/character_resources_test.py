from random import randint

from app.models.user import UserModel
from app.models.character import CharacterModel


# post to /character/new should return a character id and store a character in the database
def test_character_new_post(app, auth, populate_db):
    auth.login('test', 'test')
    response = auth.post('/character/new', {'name': 'test'})

    assert response.status_code == 200
    with app.app_context():
        assert CharacterModel.get_by_id(response.get_json()['id'])


# get to /character/<char_id> should return json with minimum of id and owner
def test_character_get(auth, populate_db):
    auth.login('test', 'test')
    response = auth.get(f'/character/get/{populate_db["characterId"]}')
    json = response.get_json()

    assert response.status_code == 200
    assert 'id' in json and 'owner' in json


# get request to /character/<char_id> should return 400 if identity doesn't match
def test_character_get_wrong_owner(app, auth, populate_db):
    with app.app_context():
        UserModel('silly', 'bugger').add_user()
    auth.login('silly', 'bugger')
    response = auth.get(f'/character/get/{populate_db["characterId"]}')

    assert response.status_code == 400


# get request to /character/<char_id> should return 400 if no character exists
def test_character_get_no_character(app, auth):
    # have to make a user to login rather than populate_db so that there aren't characters pre-populated
    with app.app_context():
        user = UserModel('test', 'test').add_user()
    auth.login('test', 'test')
    response = auth.get('/character/get/1')

    assert response.status_code == 400


# patch request to /character/get/<char_id> should mutate character
def test_character_patch(app, auth, populate_db):
    with app.app_context():
        assert not CharacterModel.get_by_id(populate_db['characterId']).name

    auth.login('test', 'test')
    auth.patch(f'/character/get/{populate_db["characterId"]}', {'character': {'name': 'silly'}})

    with app.app_context():
        assert CharacterModel.get_by_id(populate_db["characterId"]).name == 'silly'


# patch request to /character/get/<char_id> should throw 400 if wrong owner sends request
def test_character_patch_bad_request(app, client, auth, populate_db):
    with app.app_context():
        UserModel('silly', 'bugger').add_user()
    auth.login('silly', 'bugger')

    response = auth.patch(f'/character/get/{populate_db["characterId"]}', {'name': 'silly'})

    assert response.status_code == 400


# delete request to /character/get/<char_id> should delete the db entry
def test_character_delete(app, auth, populate_db):
    with app.app_context():
        # have to make a new character rather than using populated one as the populated ability is dependent on the
        # populated character
        char_id = CharacterModel(populate_db['userId']).add_character().id
        assert CharacterModel.get_by_id(char_id)

    auth.login('test', 'test')
    auth.delete(f'/character/get/{char_id}')

    with app.app_context():
        assert not CharacterModel.get_by_id(char_id)


# delete request to /character/get/<char_id> should return 400 if user isn't owner
def test_character_delete_bad_request(app, auth, populate_db):
    with app.app_context():
        UserModel('silly', 'bugger').add_user()

    auth.login('silly', 'bugger')

    response = auth.delete(f'/character/get/{populate_db["characterId"]}')

    assert response.status_code == 400


# get request to /character/all should return list of characters
def test_character_all_get(app, auth, populate_db):
    char_amount = randint(1, 20)
    with app.app_context():
        user = UserModel('silly', 'bugger').add_user()
        for i in range(0, char_amount):
            CharacterModel(user.id).add_character()

    auth.login('silly', 'bugger')
    response = auth.get('/character/all')

    assert response.status_code == 200
    assert 'characters' in response.get_json()
    assert len(response.get_json()['characters']) == char_amount


# get request to /character/all should return 400 if no characters
def test_character_all_get_no_characters(app, auth, populate_db):
    with app.app_context():
        UserModel('silly', 'bugger').add_user()
    auth.login('silly', 'bugger')

    response = auth.get('/character/all')

    assert response.status_code == 400
