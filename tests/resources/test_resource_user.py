import json


def test_user_registration(client):
    # Testing reused username
    response = client.post(
        '/user/register',
        data=json.dumps({'username': 'test', 'password': 'test'}),
        content_type='application/json'
    )
    assert response.status_code == 400

    # Testing successful request
    response = client.post(
        '/user/register',
        data=json.dumps({'username': 'test2', 'password': 'test'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['username'] == 'test2'
    assert 'accessToken' in data
    assert 'refreshToken' in data


def test_user_login(client, auth):
    # Testing access denied without authorization
    assert client.get('/secret').status_code == 401

    # Testing user doesn't exist
    assert auth.login('test2', 'test2').status_code == 400

    # Testing user password miss match
    assert auth.login('test', 'wrong')

    # Testing correct login
    login_response = auth.login()
    login_data = json.loads(login_response.data)
    print(login_data)
    secret_response = client.get(
        '/secret',
        headers={'Authorization': 'Bearer ' + login_data['accessToken']}
    )
    assert json.loads(secret_response.data)['answer'] == 42


def test_user_get(client, auth):
    # Testing access denied
    assert client.get('/user')

    # Testing successful acquisition
    login_response = json.loads(auth.login().data)
    user_response = client.get(
        '/user',
        headers={'Authorization': 'Bearer ' + login_response['accessToken']}
    )
    assert json.loads(user_response.data)['username'] == 'test'


def test_user_available(client):
    # Tests for invalid json
    response = client.post(
        '/user/available',
        data=json.dumps({'user': 'test'}),
        content_type='application/json'
    )
    assert response.status_code == 400

    # Test unavailable username
    response = client.post(
        '/user/available',
        data=json.dumps({'username': 'test'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert not response.json['available']

    # Test unavailable username
    response = client.post(
        '/user/available',
        data=json.dumps({'username': 'test2'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.json['available']
