from pydantic import BaseModel
from fastapi import APIRouter, HTTPException



class Task(BaseModel) :
    id: int
    title: str
    completed: bool


task_router = APIRouter(prefix='/task', tags=['tasks'])

tasks:list[Task] = [
    Task(id=1, title="Eat", completed=True),
    Task(id=2, title="Code", completed=False),
    Task(id=3, title="Sleep", completed=False),
    Task(id=4, title="Repeat", completed=True),
]

@task_router.get('/lists', description='Get List of tasks')
def get_tasks() -> list[Task] :
    """ """

    global tasks
    
    return tasks


@task_router.get('/id/{id}', description='Get a task by a specific `id`')
def get_task_by_id(id: int) -> Task :
    """ """

    global tasks

    current_task = next((task for task in tasks if task.id == id),
                        None)

    if current_task is None :
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return current_task