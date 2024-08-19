def test_authentication(test_client):
    response = test_client.get('/api/cars', auth=('testuser', 'testpassword'))
    assert response.status_code == 200

    response = test_client.get('/api/cars', auth=('wronguser', 'wrongpassword'))
    assert response.status_code == 401
