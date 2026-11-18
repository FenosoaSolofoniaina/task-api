from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.utilities.exceptions import APIException
from src.utilities.init_db import initialize_database
from src.utilities.database import SessionLocal

from src.register import register_router
from src.login import login_router
from src.logout import logout_router
from src.utils import utils_router



# ============================================ APP ============================================ #
app = FastAPI(
    title="Task API",
    description="API backend for TASK Manager APP",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=[settings.FRONTEND_URL],
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
with SessionLocal() as session :
    initialize_database(session)


# ============================================ TEST APP ============================================ #
@app.get(
    '/health',
    summary="App health test",
    description="Test if app is OK and running",
)
def healthy() -> dict[str, str]:
    """ """

    return { "message": "Everything is OK" }



# ============================================ ROUTES ============================================ #
prefix = settings.ROUT_PREFIX
app.include_router(register_router, prefix=prefix)
app.include_router(login_router, prefix=prefix)
app.include_router(logout_router, prefix=prefix)
app.include_router(utils_router, prefix=prefix)