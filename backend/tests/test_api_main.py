
import json

MIMETYPE = 'application/json'

def test_api(client):
    exp_result = { 'message': 'Hello API.' }
    resp = client.get('/api/')
    assert exp_result == json.loads(resp.data)
