from fastapi import FastAPI
from pydantic import BaseModel


class Task(BaseModel) :
    id: int
    title: str
    completed: bool



app = FastAPI(
    title="Task API",
    description="Test an API that manage tast using FastAPI",
    version="1.0.0"
)

tasks:list[Task] = [
    Task(id=0, title="Eat", completed=True),
    Task(id=1, title="Code", completed=False),
    Task(id=2, title="Sleep", completed=False),
    Task(id=3, title="Repeat", completed=True),
]


@app.get('/health')
def healthy() -> dict[str, str]:
    """ """

    return { "message": "Everything is OK" }


@app.get('/tasks')
def get_tasks() -> list[Task] :
    """ """

    global tasks
    
    return tasks