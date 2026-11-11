import json
from typing import Annotated

from fastapi import APIRouter, Request, status
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.config import settings
from src.security import check_rate_limit, verify_password, encode_token
from src.exceptions import DataBaseException, RessourceNotFoundException, CredentialsException
from src.models import UserAccount, UserSession
from src.database import get_db_session

from src.login.schema import TokenOut



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
def user_authentificate(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_db_session)]
) -> TokenOut:
    
    """ """

    check_rate_limit(request)
    
    user_account = UserAccount.get_account_by_identity(session=session,
                                                       identity=form_data.username)

    if user_account and verify_password(form_data.password, user_account.password_hashed):
        try :
            access_token = encode_token(user_account.user_id)
            new_session = UserSession(user_id=user_account.user_id, access_token=access_token)
            new_session.create_session(session=session)
            
            return TokenOut(access_token=access_token)

        except IntegrityError :
            session.rollback()

            raise DataBaseException(
                status_code=status.HTTP_409_CONFLICT,
                code="DUPLICATE_ERROR",
                message="The user could not be created because a database constraint was violated."
            ) from None
        
        except SQLAlchemyError :
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