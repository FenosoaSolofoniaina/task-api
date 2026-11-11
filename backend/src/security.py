import time
import datetime as dt
import jwt
from collections import defaultdict, deque
from threading import Lock
from typing import Any, Literal
from fastapi import Request, status
from pwdlib import PasswordHash

from src.config import settings
from src.exceptions import ClientBehaviourException
from src.models import UserAccount



_MAX_WINDOW_ATTEMPTS = settings.MAX_ATTEMPTS
_WINDOW_SECONDS = settings.DURATION_ATTEMPTS_SECONDS

_attempts: dict[str, deque[float]] = defaultdict(deque)
_lock = Lock()



def check_rate_limit(request: Request) -> None:
    """ """
    
    client = request.client
    if client is None:
        raise ClientBehaviourException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="IDENTITY_ERROR",
            message="Unable to identify client",
        )

    now_ = time.monotonic()

    with _lock:
        attempts = _attempts[client.host]

        # Supprimer les tentatives hors de la fenêtre
        while attempts and now_ - attempts[0] >= _WINDOW_SECONDS:
            attempts.popleft()

        if len(attempts) >= _MAX_WINDOW_ATTEMPTS:
            raise ClientBehaviourException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                code="REQUEST_ERROR",
                message="Too many authentication attempts. Try again later."
            )

        # Compter cette requête
        attempts.append(now_)



def encode_token(
    user_id: int,
    token_type: Literal['access', 'refresh'] = 'access'
) -> str:
    """ """

    now_ = dt.datetime.now(tz=dt.timezone.utc)
    #token_ttl = dt.timedelta(minutes=settings.ACCESS_TOKEN_TTL) if token_type=='access' else dt.timedelta(days=settings.REFRESH_TOKEN_TTL)
    token_ttl = dt.timedelta(minutes=settings.ACCESS_TOKEN_TTL)
    

    payload = {
        "sub": str(user_id),
        "type": f"{token_type}_token",
        "iat": now_,
        "exp": now_ + token_ttl,
    }

    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token



def decode_token(token: str) -> dict[str, Any]:
    """ """

    decoded_token = jwt.decode(
        token,
        key=settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM]
    )

    return decoded_token




password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str :
    """ """

    return password_hasher.hash(password=password)



def verify_password(password: str, password_hashed: str) -> bool :
    """ """
    
    return password_hasher.verify(password, password_hashed) 