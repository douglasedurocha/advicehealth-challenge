import json

def test_get_owners(test_client, init_database):
    response = test_client.get('/api/owners', auth=('testuser', 'testpassword'))
    print(response.data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'owners' in data

def test_get_owner(test_client, init_database):
    response = test_client.get('/api/owners/1', auth=('testuser', 'testpassword'))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'John Doe'

def test_post_owner(test_client, init_database):
    response = test_client.post('/api/owners', 
                                json={'name': 'John Doe'}, 
                                auth=('testuser', 'testpassword'))
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'John Doe'

def test_put_owner(test_client, init_database):
    response = test_client.put('/api/owners/1', 
                               json={'name': 'Jane Doe'}, 
                               auth=('testuser', 'testpassword'))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Jane Doe'

def test_delete_owner(test_client, init_database):
    response = test_client.delete('/api/owners/1', auth=('testuser', 'testpassword'))
    assert response.status_code == 200

def test_cascade_delete_owner(test_client, init_database):
    response = test_client.get('/api/owners/1', auth=('testuser', 'testpassword'))
    assert response.status_code == 404

    response = test_client.get('/api/cars', auth=('testuser', 'testpassword'))
    data = json.loads(response.data)
    assert data['count'] == 0
    assert not data['cars']