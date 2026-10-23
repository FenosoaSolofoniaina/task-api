from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.login import login_router



# ============================================ APP ============================================ #
app = FastAPI(
    title="Task API",
    description="Test an API that manage tast using FastAPI",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=[
        'http://localhost:5173'
    ],
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=['Content-Type', 'Accept', 'Authorization']
)
# ============================================ TEST ENDPOINT ============================================ #
@app.get('/health', description="Test if app is OK and running")
def healthy() -> dict[str, str]:
    """ """

    return { "message": "Everything is OK" }


# ============================================ ROUTERS ============================================ #
app.include_router(login_router)