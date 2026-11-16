import json
import uuid
from typing import Annotated
from fastapi import APIRouter, Request, status, Response
from fastapi import Depends
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.config import settings
from src.security import check_rate_limit, verify_password, create_access_token
from src.exceptions import DataBaseException, RessourceNotFoundException, CredentialsException
from src.models import UserAccount, UserSession
from src.database import get_db_session

from src.login.schema import LoginRequest, LoginResponse



# ============================================ ROUTER ============================================ #
login_router = APIRouter(
    prefix='/login',
    tags=['Login']
)

# ============================================ ENDPOINTS ============================================ #
# =========================================================
# FORM STRUCTURE
# =========================================================
@login_router.get(
    '/forms',
    summary="Login Forms template",
    description="Get the form template of the Task Manager App"
)
def get_forms_template() -> list[dict]:
    """ """

    try :
        with open(settings.PROJECT_JSON_DIR / "loginForms.json", 'r') as json_file :
            return json.load(json_file)
        
    except FileNotFoundError :
        raise RessourceNotFoundException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            code="NOT_FOUND",
            message="Resssource not found. Data on server not available or empty"
        )


# =========================================================
# AUTHENTIFICATION
# =========================================================
@login_router.post(
    '/',
    summary="App Authentification",
    description="User authentification using `payload`",
    status_code=status.HTTP_201_CREATED,
)
def user_login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    session: Annotated[Session, Depends(get_db_session)]
) -> LoginResponse:
    
    """ """

    check_rate_limit(request)

    result = LoginResponse()
    
    user_account = UserAccount.get_account_by_identity(session=session,
                                                       identity=payload.identity)

    if user_account and verify_password(payload.password, user_account.password_hashed):
        try :
            session_id = uuid.uuid4()
            access_token = create_access_token(user_id=user_account.user_id, session_id=str(session_id))
            new_session = UserSession(
                id=session_id,
                user_id=user_account.user_id,
                access_token=access_token
            )
            result.success = True
            result.response = new_session.create(session=session)

            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="lax",
                max_age=settings.ACCESS_TOKEN_TTL * 60
            )

            return result

        except IntegrityError :
            session.rollback()

            raise DataBaseException(
                status_code=status.HTTP_409_CONFLICT,
                code="DUPLICATE_ERROR",
                message="The user could not be created because a database constraint was violated."
            ) from None
        
        except SQLAlchemyError as e:
            session.rollback()
            raise DataBaseException(
                status_code=status.HTTP_409_CONFLICT,
                code="DATABASE_ERROR",
                message="A database error occurred."
            ) from None


    else :
        raise CredentialsException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTHENTIFICATION_ERROR",
            message="Account not found or password not correct"

        ) from None