from typing import Annotated
from fastapi import status
from fastapi import Depends, Cookie
from sqlalchemy.orm import Session
from jwt import InvalidTokenError, ExpiredSignatureError

from src.database import get_db_session
from src.models import UserSession
from src.security import decode_access_token
from src.exceptions import CredentialsException



def get_current_session(
    session: Annotated[Session, Depends(get_db_session)],
    token: str | None = Cookie(default=None, alias='access_token'),
) -> "UserSession" :
    """ """

    if token is None :
        raise CredentialsException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTHENTIFICATION_ERROR",
            message="Empty token is invalid"
        ) from None

    try :
        payload = decode_access_token(token=token)

    except ExpiredSignatureError :
        UserSession.revoke_session_by_token(session=session, token=token)
        raise CredentialsException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTHENTIFICATION_ERROR",
            message="Expired token"
        ) from None
    
    except InvalidTokenError :
        raise CredentialsException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTHENTIFICATION_ERROR",
            message="Invalide token"
        ) from None


    user_id = int(payload.get('sub'))
    
    if user_id is None :
        raise CredentialsException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        code="AUTHENTIFICATION_ERROR",
        message="User not found"
    ) from None


    return UserSession.get_active_session(
        session=session,
        user_id=user_id
    )
