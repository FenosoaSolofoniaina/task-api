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


# ========================================== GET ========================================== #
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


# ========================================== POST ========================================== #
@task_router.post('/add/', description='Add a new task')
def add_task(title: str | None = None,
             completed: bool | None = None) -> Task :
    """ """

    global tasks

    if title is None or completed is None :
        raise HTTPException(
            status_code=400,
            detail="Value `title` and `completed` must be specified"
        )
    
    new_task = Task(id=len(tasks) + 1, title=title, completed=completed)
    tasks.append(new_task)

    return new_task


# ========================================== PUT(update) ========================================== #
@task_router.put('/update/id/{id}', description='Update a task by specifing `id`')
def update_task_by_id(id: int,
                      title: str | None = None,
                      completed: bool | None = None) -> Task :
    """ """

    global tasks

    if title is None and completed is None :
        raise HTTPException(
            status_code=501,
            detail="At least `title` or `completed` must have value"
        )

    current_task = next((task for task in tasks if task.id == id),
                            None)

    if current_task is None :
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if title is not None :
        current_task.title = title
    if completed is not None :
            current_task.completed = completed

    return current_task


# ========================================== DELETE ========================================== #
@task_router.delete('/delete/id/{id}', description='Remove a task by specifing `id`')
def remove_task_by_id(id: int) -> Task :
    """ """

    global tasks

    current_task = next((task for task in tasks if task.id == id),
                            None)

    if current_task is None :
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    tasks.remove(current_task)

    return current_task