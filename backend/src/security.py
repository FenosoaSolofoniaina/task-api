import time
import datetime as dt
from collections import defaultdict, deque
from threading import Lock
from typing import Any
from fastapi import Request, status

from src.config import settings
from src.exceptions import ClientBehaviourException


# =========================================================
# Maximum rate limite
# =========================================================
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



# =========================================================
# Encode/decode token
# =========================================================
import jwt


def create_access_token(user_id: int, session_id: str) -> str:
    """ """

    now_ = dt.datetime.now(tz=dt.timezone.utc)
    token_ttl = dt.timedelta(minutes=settings.ACCESS_TOKEN_TTL)
    
    payload = {
        "sub": str(user_id),
        "sid": session_id,
        "type": "access_token",
        "iat": now_,
        "exp": now_ + token_ttl,
    }

    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def decode_access_token(token: str, verify_exp: bool=True) -> dict[str, Any]:
    """ """

    decoded_token = jwt.decode(
        token,
        key=settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        options={"verify_exp": verify_exp}
    )

    return decoded_token



# =========================================================
# Encode/decode password
# =========================================================
from pwdlib import PasswordHash


password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str :
    """ """

    return password_hasher.hash(password=password)


def verify_password(password: str, hash: str) -> bool :
    """ """
    
    return password_hasher.verify(password, hash) 