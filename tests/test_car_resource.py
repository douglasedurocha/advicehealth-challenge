import json
import pytest

def test_get_cars(test_client, init_database):
    response = test_client.get('/api/cars', auth=('testuser', 'testpassword'))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'count' in data
    assert 'cars' in data

def test_post_car_without_owner(test_client, init_database):
    response = test_client.post('/api/cars', 
                                json={'color': 'gray', 'model': 'sedan', 'owner_id': 0}, 
                                auth=('testuser', 'testpassword'))
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Owner with ID' in data['message']

def test_post_car_with_invalid_color(test_client, init_database):
    response = test_client.post('/api/cars', 
                                json={'color': 'black', 'model': 'sedan', 'owner_id': 1}, 
                                auth=('testuser', 'testpassword'))
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Invalid color' in data['message']

def test_post_car_with_invalid_model(test_client, init_database):
    response = test_client.post('/api/cars', 
                                json={'color': 'blue', 'model': 'coupe', 'owner_id': 1}, 
                                auth=('testuser', 'testpassword'))
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Invalid model' in data['message']

def test_post_car(test_client, init_database):
    response = test_client.post('/api/cars', 
                                json={'color': 'gray', 'model': 'sedan', 'owner_id': 1}, 
                                auth=('testuser', 'testpassword'))
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['color'] == 'gray'
    assert data['model'] == 'sedan'
    assert data['owner_id'] == 1

def test_put_car(test_client, init_database):
    response = test_client.post('/api/cars', 
                                json={'color': 'blue', 'model': 'sedan', 'owner_id': 1}, 
                                auth=('testuser', 'testpassword'))
    assert response.status_code == 201
    
    response = test_client.put('/api/cars/1', 
                               json={'color': 'yellow'}, 
                               auth=('testuser', 'testpassword'))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['color'] == 'yellow'

def test_delete_car(test_client, init_database):
    response = test_client.post('/api/cars', 
                                json={'color': 'blue', 'model': 'sedan', 'owner_id': 1}, 
                                auth=('testuser', 'testpassword'))
    assert response.status_code == 201
    
    response = test_client.delete('/api/cars/1', auth=('testuser', 'testpassword'))
    assert response.status_code == 204
