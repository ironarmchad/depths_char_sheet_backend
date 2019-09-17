# get '/hello' return a json with a message
def test_hello(client):
    response = client.get('/hello').json
    assert 'message' in response
