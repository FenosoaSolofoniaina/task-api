def test_app_is_running(client) :
    """ """

    response = client.get('/health')

    assert response.status_code == 200
    assert response.json() == { "message": "Everything is OK" }