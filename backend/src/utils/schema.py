from pydantic import BaseModel, ConfigDict
from typing import Any



# ================================================================================ #
# Login account
# ================================================================================ #
class LoginRequest(BaseModel) :
    """ """

    model_config = ConfigDict(extra="forbid")

    identity: str
    password: str


# ================================================================================ #
# Response from login
# ================================================================================ #
class LoginResponse(BaseModel) :
    """ """

    success: bool = False
    response: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
