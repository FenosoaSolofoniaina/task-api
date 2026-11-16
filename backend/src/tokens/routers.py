from uuid import uuid4
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

from src.config import settings
from src.models import UserSession
from src.security import create_access_token



token_router = APIRouter(
    prefix=f'{settings.ROUT_PREFIX}/token',
    tags=['token', 'authnetification']
)


@token_router.post(
    '/create',
    summary="",
    description="",
    status_code=status.HTTP_201_CREATED
)
def create_new_session(user_id: int,
                       form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
                       access_token: str) -> "UserSession" :
    """ """

    session_id = str(uuid4())
    access_token = create_access_token(user_id, session_id)

    
    return UserSession(id=session_id,
                       user_id=user_id,
                       access_token=access_token)