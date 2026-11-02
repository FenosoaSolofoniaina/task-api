from fastapi import FastAPI, APIRouter
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.exceptions import APIException
from src.config import settings
from src.init_db import init_country_db, init_role_db
from src.database import engine, Base, SessionLocal
from src.routers.register import register_router
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
    allow_origins=[settings.FRONTENT_URL],
    allow_methods=['GET', 'POST', 'DELETE', 'PUT'],
    allow_headers=['Content-Type', 'Accept', 'Authorization']
)

@app.exception_handler(APIException)
async def api_exception_handler(
    request: Request,
    exc: APIException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.error_response,
    )


# ============================================ INIT DATABASE ============================================ #
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
with SessionLocal() as session :
    init_country_db(session)
    init_role_db(session)
    
# ============================================ TEST APP ============================================ #
api_router = APIRouter(prefix='/api/v1')
@api_router.get(
    '/health',
    summary="App health test",
    description="Test if app is OK and running",
)
def healthy() -> dict[str, str]:
    """ """

    return { "message": "Everything is OK" }


# ============================================ ROUTES ============================================ #
api_router.include_router(register_router)
api_router.include_router(login_router)

# MAIN ROUTER
app.include_router(api_router)