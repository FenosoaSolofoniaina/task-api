from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
from fastapi import Depends
from sqlalchemy.orm import Session
from jwt import InvalidTokenError

from src.config import settings
from src.database import get_db_session
from src.models import UserSession
from src.security import decode_token
from src.exceptions import CredentialsException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.ROUT_PREFIX}/login")


async def get_current_session(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_db_session)]
) -> "UserSession" :
    """ """

    try :
        payload = decode_token(token=token)

    except InvalidTokenError :
        raise CredentialsException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        code="AUTHENTIFICATION_ERROR",
        message="Invalide token or expired"
    ) from None


    user_id = int(payload.get('sub'))
    
    if user_id is None :
        raise CredentialsException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        code="AUTHENTIFICATION_ERROR",
        message="User_id not found"
    ) from None


    return UserSession.get_session_by_user_id(session=session, user_id=user_id)
