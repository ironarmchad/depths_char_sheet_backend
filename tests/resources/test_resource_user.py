import json


def test_all_users(client):
    response = client.get('/user')
    data = json.loads(response.data)
    assert response.status_code == 200
    print(data)
    assert data['users'][0]['username'] == 'test'


def test_user_registration(client):
    # Testing reused username
    assert client.post('/user/register', data={'username': 'test', 'password': 'test'}).status_code == 400

    # Testing successful request
    response = client.post('/user/register', data={'username': 'test2', 'password': 'test'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['username'] == 'test2'
    assert 'access-token' in data
    assert 'refresh-token' in data


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
