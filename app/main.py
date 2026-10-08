import os
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Task API",
    description="Test an API that manage tast using FastAPI",
    version="1.0.0"
)


@app.get('/health')
def healthy() -> dict[str, str]:
    """ """

    return { "message": "Everything is OK" }


@app.get('/tasks')
def get_tasks() -> list[str] :
    """ """

    return []