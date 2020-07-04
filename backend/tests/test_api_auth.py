import json

MIMETYPE = 'application/json'

def test_api_auth_login_succ(client):
    headers = {
        'Content-Type': MIMETYPE,
        'Accept': MIMETYPE
    }
    data = {
        'username': 'user',
        'password': 'pass'
    }
    response = client.post('/api/login', data=json.dumps(data), headers=headers)
    result = json.loads(response.data)
    assert 'access_token' in result, 'access token missing'
    assert len(result['access_token']) > 0, 'access token missing'
    assert 'refresh_token' in result, 'refresh token missing'
    assert len(result['refresh_token']) > 0, 'refresh token missing'

def test_api_auth_login_fail(client):
    headers = {
        'Content-Type': MIMETYPE,
        'Accept': MIMETYPE
    }
    data = {
        'username': 'usr',
        'password': 'pwd'
    }
    response = client.post('/api/login', data=json.dumps(data), headers=headers)
    assert response.status_code == 401, 'invalid user credentials'
    result = json.loads(response.data)


def test_api_auth_refresh_succ(client):
    headers = {
        'Content-Type': MIMETYPE,
        'ACCEPT': MIMETYPE
    }
    data = {
        'username': 'user',
        'password': 'pass'
    }
    response = client.post('/api/login', data=json.dumps(data), headers=headers)
    result = json.loads(response.data)
    refresh_token = result['refresh_token']

    headers['Authorization'] = f'Bearer {refresh_token}'
    data = {}
    response = client.post('/api/refresh', data=json.dumps(data), headers=headers)
    assert response.status_code == 201, 'invalid user credentials'
    result = json.loads(response.data)
    assert 'access_token' in result, 'access token missing'
    assert len(result['access_token']) > 0, 'access token missing'

def test_api_auth_refresh_fail(client):
    headers = {
        'Content-Type': MIMETYPE,
        'ACCEPT': MIMETYPE
    }
    data = {}
    response = client.post('/api/refresh', data=json.dumps(data), headers=headers)
    assert response.status_code == 401, 'invalid user credentials'
    result = json.loads(response.data)
