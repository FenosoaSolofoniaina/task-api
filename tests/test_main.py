from fastapi.testclient import TestClient

from app.main import app



client = TestClient(app)


def test_app_is_running() :
    """ """

    response = client.get('/health')

    assert response.status_code == 200
    assert response.json() == { "message": "Everything is OK" }


def test_get_list_tasks() :
    """ """

    response = client.get('/tasks')

    assert response.status_code == 200
    assert response.json() != []