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

    response = client.get('/task/lists')

    assert response.status_code == 200
    assert response.json() != []


def test_get_task_by_id() :
    """ """

    response = client.get('/task/id/99')
    assert response.status_code == 404
    assert response.json() == { 'detail': "Task not found" }

    response = client.get('/task/id/1')
    
    assert response.status_code == 200
    assert response.json() != { 'detail': "Task not found" }