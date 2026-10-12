import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.tasks import Task, tasks



@pytest.fixture(autouse=True)
def reset_task() -> None :
    """ """

    tasks.clear()
    tasks.extend([
        Task(id=1, title="Eat", completed=True),
        Task(id=2, title="Code", completed=False),
        Task(id=3, title="Sleep", completed=False),
        Task(id=4, title="Repeat", completed=True),
    ])


@pytest.fixture
def client() -> TestClient :
    return TestClient(app)
