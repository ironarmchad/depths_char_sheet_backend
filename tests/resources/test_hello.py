import json


def test_hello(client):
    response = client.get('/hello')
    assert json.loads(response.data)['message'] == 'Hello, World?'
