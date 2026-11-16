import datetime as dt
from typing import Any
from pydantic import BaseModel, ConfigDict
from pydantic import Field, field_validator
from fastapi import status

from src.exceptions import DataValueException



# ================================================================================ #
# Register account and profil
# ================================================================================ #
class RegisterMeSchema(BaseModel) :
    """ """

    model_config = ConfigDict(extra="forbid")

    firstname: str = Field(min_length=2, max_length=60, strict=True)
    lastname: str = Field(min_length=2, max_length=60, strict=True)
    sexe: str = Field(min_length=1, max_length=1, strict=True)
    birth: dt.date = Field()
    email: str = Field(min_length=1, max_length=60, strict=True)
    country_id: int = Field(gt=0, lt=300, strict=True)

    @field_validator("birth")
    @classmethod
    def validate_birth(cls,
                       value: dt.date) -> dt.date:

        MIN_AGE = 10 # ans
        today = dt.date.today()

        # 1. Interdire une date dans le futur
        if value > today:
            raise DataValueException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                code="FUTUR_DATE_ERROR",
                message="The date of birth cannot be in the future."
            )

        # 2. Calculer l'âge réel
        age = today.year - value.year
        if (today.month, today.day) < (value.month, value.day):
            age -= 1

        # 3. Imposer un âge minimum
        if age < MIN_AGE:
            raise DataValueException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                code="MINIMUM_AGE_ERROR",
                message="You don't have required age."
            )

        return value



class RegisterAccountSchema(BaseModel) :
    """ """

    model_config = ConfigDict(extra="forbid")

    user_id: int = Field(gt=0, strict=True)
    identity: str = Field(min_length=5, max_length=50, strict=True)
    password: str = Field(min_length=8, max_length=30, strict=True)



class RegisterDataOutput(BaseModel) :
    """ """

    success: bool = False
    response: dict[str, Any] | None = None
    error: dict[str, Any] | None = None