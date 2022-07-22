import json


def test_create_user(client):
    data = {'username': 'testuser', 'email': 'testuser@mail.com', 'password': 'test123'}
    response = client.post('/users/', json.dumps(data))
    assert response.status_code == 200
    assert response.json()['email'] == 'testuser@mail.com'
    assert response.json()['is_active']
