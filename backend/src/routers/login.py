import json
from typing import Annotated
from pwdlib import PasswordHash
from fastapi import APIRouter, Request
from fastapi import status
from fastapi import Header, Body
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.config import settings
from src.security import check_rate_limit
from src.schemas import LoginAuthInput, LoginAuthOutput
from src.exceptions import RequestHeaderException, DataBaseException
from src.models import UserAccount, UserSession
from src.database import SessionLocal



password_hasher = PasswordHash.recommended()

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

    with open(settings.PROJECT_JSON_DIR / "loginForms.json", 'r') as json_file :
        return json.load(json_file)



# =========================================================
# AUTHENTIFICATION
# =========================================================
@login_router.post(
    '/auth',
    summary="Authentification",
    description="User authentification using `payload`"
)
def user_authentificate(
    request: Request,
    payload: Annotated[
        LoginAuthInput,
        Body()
    ],
    content_type: str = Header(..., alias='Content-Type')
) -> LoginAuthOutput:
    
    """ """

    check_rate_limit(request)

    result = LoginAuthOutput()

    if content_type != "application/json" :
        raise RequestHeaderException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            code="UNSUPPORTED_MEDIA_TYPE",
            message="Request media type is not acceptable"
        )

    with SessionLocal() as session :
        user_account = UserAccount.get_user_by_identity(session=session,
                                                        identity=payload.identity)

        if user_account and password_hasher.verify(payload.password, user_account.password_hashed) :
            try :
                user_session = UserSession.create_session(session=session, account=user_account)
                result.success = True
                result.response = {
                    'access_token': user_session.access_token,
                    'refresh_token': user_session.refresh_token,
                    'token_type': user_session.token_type
                }
            except IntegrityError :
                    raise DataBaseException(
                        status_code=status.HTTP_409_CONFLICT,
                        code="DUPLICATE_ERROR",
                        message="The user could not be created because a database constraint was violated."
                    ) from None
            
            except SQLAlchemyError :
                raise DataBaseException(
                    status_code=status.HTTP_409_CONFLICT,
                    code="DATABASE_ERROR",
                    message="A database error occurred."
                ) from None


        else :
            result.error = {
                'code': 'AUTHENTIFICATION_ERROR',
                'message': 'Account not found or password not correct',
            }    

        return result