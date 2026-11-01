import datetime as dt
import jwt
from typing import Any, Literal

from src.config import settings



def encode_token(
    account: Any,
    token_type: Literal['access', 'refresh'] = 'access'
) -> str:
    """ """

    now_ = dt.datetime.now(tz=dt.timezone.utc)
    token_ttl = dt.timedelta(days=settings.ACCESS_TOKEN_TTL) if token_type=='access' else dt.timedelta(days=settings.REFRESH_TOKEN_TTL)

    payload = {
        "uid": account.user_id,
        "identity": account.identity,
        "type": token_type,
        "iat": now_,
        "exp": now_ + token_ttl
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