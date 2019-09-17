import json

from app.models.user import UserModel


# get request to /user/# should return json with username
def test_user_get(client, auth, populate_db):
    jwt = auth.login('test1', 'test').json
    response = client.get(
        '/user',
        headers={'Authorization': 'Bearer ' + jwt['accessToken']}
    ).json

    assert response['username'] == 'test1'


# post request to /user/available with the possible username will return json with
# "available": True if username not in use
def test_user_available_post_true(client, populate_db):
    # populate db defines test1, test2 and test3 I shall see if 'silly' is available
    response = client.post(
        '/user/available',
        content_type='application/json',
        data=json.dumps({'username': 'silly'})
    ).get_json()

    assert response['available']


# post request to /user/available with the possible username should return json with
# "available": False if username is in use
def test_user_available_post_false(client, populate_db):
    # since test1 is already in db I will use test1
    response = client.post(
        '/user/available',
        content_type='application/json',
        data=json.dumps({'username': 'test1'})
    ).get_json()

    assert not response['available']


# post request to /user/register without username and password should return a 400 error
def test_user_register_invalid(client):
    response = client.post(
        '/user/register',
        content_type='application/json',
        data=json.dumps({'name': 'test', 'code': 'test'})
    )

    assert response.status_code == 400


# post request to /user/register using an already claimed username should return a 400 error
def test_user_register_unique_error(client, populate_db):
    response = client.post(
        '/user/register',
        content_type='application/json',
        data=json.dumps({'username': 'test1', 'password': 'test'})
    )

    assert response.status_code == 400


# post request to /user/register should make a db entry with new user (if successful)
def test_user_register(app, client):
    response = client.post(
        '/user/register',
        content_type='application/json',
        data=json.dumps({'username': 'test', 'password': 'test'})
    )

    assert response.status_code == 200

    with app.app_context():
        assert UserModel.find_by_username('test')


# post to /user/login that doesn't have username or password should return 400
def test_user_login_bad_data(client):
    resp_no_username = client.post(
        '/user/login',
        content_type='application/json',
        data=json.dumps({'password': 'test'})
    )

    resp_no_password = client.post(
        '/user/login',
        content_type='application/json',
        data=json.dumps({'username': 'test'})
    )

    assert resp_no_password.status_code == 400
    assert resp_no_username.status_code == 400


# post to /user/login should return 400 if user doesn't exist yet
def test_user_login_no_user(client, populate_db):
    response = client.post(
        '/user/login',
        content_type='application/json',
        data=json.dumps({'username': 'silly', 'password': 'test'})
    )

    assert response.status_code == 400


# post to /user/login should return 400 if user provides bad password
def test_user_login_bad_password(client, populate_db):
    response = client.post(
        '/user/login',
        content_type='application/json',
        data=json.dumps({'username': 'test1', 'password': 'silly'})
    )

    assert response.status_code == 400


# post to /user/login should return json with accessToken if successful
def test_user_login(client, populate_db):
    response = client.post(
        '/user/login',
        data=json.dumps({'username': 'test1', 'password': 'test'}),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert 'accessToken' in response.get_json()
