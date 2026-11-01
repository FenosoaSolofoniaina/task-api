import time
from collections import defaultdict, deque
from threading import Lock

from fastapi import Request, status

from src.exceptions import ClientBehaviourException
from src.config import settings


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