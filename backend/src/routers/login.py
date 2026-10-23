from pydantic import BaseModel
from fastapi import APIRouter, Header, HTTPException, status, Request
from datetime import datetime as dt, timedelta, timezone
from pwdlib import PasswordHash
import jwt

from src.config import settings
from src.security.rate_limit import check_rate_limit


password_hasher = PasswordHash.recommended()

# ============================================ ROUTER ============================================ #
login_router = APIRouter(
    prefix='/login',
    tags=['Login']
)


# ============================================ FORM STRUCTURE ============================================ #
class LoginInputForm(BaseModel) :
    id: str
    type: str
    placeholder: str
    title: str
    text: str
    required: bool


@login_router.get(
    '/forms',
    description="Get the form template of the Task Manager App"
)
def get_login_forms() -> list[LoginInputForm]:
    """ """
    
    return [
        {
            "id": "identity",
            "type": "text",
            "placeholder": "",
            "title": "Identifiant",
            "text": "Identifiant",
            "required": True,
        },
        {
            "id": "password",
            "type": "password",
            "placeholder": "",
            "title": "Mot de passe",
            "text": "Mot de passe",
            "required": True,
        },
    ]


# ============================================ AUTHENTIFICATION ============================================ #
class UserAuthInput(BaseModel) :
    identity: str
    password: str
    timestamp: int


class UserAuthResponse(BaseModel) :
    authenticate: bool
    user_id: int | None = None
    access_token: str | None = None
    expire_at: int | None = None
    timestamp: int


@login_router.post(
        '/auth',
        description="User authentification")
def user_authentificate(
    request: Request,
    payload: UserAuthInput,
    content_type: str = Header(..., alias='Content-Type')
) -> UserAuthResponse:
    
    """ """

    check_rate_limit(request)

    response = UserAuthResponse(authenticate=False, timestamp=payload.timestamp)

    users_identity = [
        {
            "user_id": 100,
            "identity": "john.doe",
            "password_hashed": password_hasher.hash("myNameIsJohn2e")
        },
        {
            "user_id": 101,
            "identity": "maire.pipeline",
            "password_hashed": password_hasher.hash("marieIssoCut3")
        }
    ]

    if content_type != "application/json" :
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Request media type is not acceptable"
        )

    current_user = next(
        (user for user in users_identity if (
                user['identity'] == payload.identity and 
                password_hasher.verify(payload.password, user['password_hashed'])
            )
        ),
        None
    )

    if current_user is not None :

        now_ = dt.now(tz=timezone.utc)
        expire = int((now_ + timedelta(hours=settings.TOKEN_TTL)).timestamp())
        user_id = current_user['user_id']
        
        # Generate token
        token = jwt.encode(
            payload={
                "sub": user_id,
                "iat": now_,
                "exp": expire
            },
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

        # Generate response
        response = UserAuthResponse(
            authenticate=True,
            user_id=user_id,
            access_token=token,
            expire_at=expire,
            timestamp=payload.timestamp
        )

    return response