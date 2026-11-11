from typing import Annotated
from fastapi import APIRouter, status
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.models import UserSession
from src.exceptions import DataBaseException
from src.database import get_db_session
from src.dependencies import get_current_session

from src.logout.schema import LogoutOutput



# ============================================ ROUTER ============================================ #
logout_router = APIRouter(
    prefix='/logout',
    tags=['Logout']
)

# ============================================ ENDPOINTS ============================================ #

# =========================================================
# LOGOUT
# =========================================================
@logout_router.post(
    '/',
    summary="Login out",
    description="User logged out. Session closed and removed"
)
def user_logout(
    current_session: Annotated[UserSession, Depends(get_current_session)],
    session: Annotated[Session, Depends(get_db_session)],
) -> LogoutOutput:

    result = LogoutOutput()

    try :
        result.response = current_session.remove_session(session=session)
        result.success = True

        return result

    except SQLAlchemyError as e:
        session.rollback()

        raise DataBaseException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="DATABASE_ERROR",
            message="A database error occurred."
        ) from None