from fastapi import FastAPI

from app.routers.tasks import task_router



app = FastAPI(
    title="Task API",
    description="Test an API that manage tast using FastAPI",
    version="1.0.0"
)

@app.get('/health', description="Test if app is OK and running")
def healthy() -> dict[str, str]:
    """ """

    return { "message": "Everything is OK" }


app.include_router(task_router)