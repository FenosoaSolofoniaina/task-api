from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic import Field



# ================================================================================ #
# Logout account
# ================================================================================ #
class LogoutOutput(BaseModel) :
    """ """

    success: bool = False
    response: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
