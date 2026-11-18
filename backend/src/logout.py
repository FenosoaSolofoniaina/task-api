from typing import Annotated, Any
from fastapi import APIRouter, status, Response
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from src.models import UserSession
from src.utilities.exceptions import DataBaseException
from src.utilities.database import get_db_session
from src.utilities.dependencies import get_current_session



# ============================================ ROUTER ============================================ #
logout_router = APIRouter(
    prefix='/logout',
    tags=['Logout']
)


# ============================================ SCHEMAS ============================================ #
# ================================================================================ #
# Logout account
# ================================================================================ #
class LogoutResponse(BaseModel) :
    """ """

    success: bool = False
    response: dict[str, Any] | None = None
    error: dict[str, Any] | None = None



# ============================================ ENDPOINTS ============================================ #
# =========================================================
# LOGOUT
# =========================================================
@logout_router.post(
    '/',
    summary="Logout",
    description="User logged out. Session closed and removed"
)
def user_logout(
    current_session: Annotated[UserSession, Depends(get_current_session)],
    response: Response,
    session: Annotated[Session, Depends(get_db_session)],
) -> LogoutResponse:

    result = LogoutResponse()

    try :
        result.response = current_session.revoke(session=session)
        result.success = True
        response.delete_cookie('access_token')

        return result

    except SQLAlchemyError as e:
        session.rollback()

        raise DataBaseException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="DATABASE_ERROR",
            message="A database error occurred."
        ) from None