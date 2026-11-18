import datetime as dt
from typing import Annotated, Any
from fastapi import APIRouter, status
from fastapi import Body, Header, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import BaseModel, ConfigDict
from pydantic import Field, field_validator

from src.models import UserInfo, UserAccount
from src.utilities.exceptions import DataBaseException, RequestHeaderException, DataValueException
from src.utilities.database import get_db_session
from src.utilities.security import hash_password



# ============================================ ROUTER ============================================ #
register_router = APIRouter(
    prefix='/register',
    tags=['Register']
)


# ============================================ SCHEMAS ============================================ #
# ================================================================================ #
# Register account and profil
# ================================================================================ #
class RegisterMeRequest(BaseModel) :
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



class RegisterAccountRequest(BaseModel) :
    """ """

    model_config = ConfigDict(extra="forbid")

    user_id: int = Field(gt=0, strict=True)
    identity: str = Field(min_length=5, max_length=50, strict=True)
    password: str = Field(min_length=8, max_length=30, strict=True)



class RegisterResponse(BaseModel) :
    """ """

    success: bool = False
    response: dict[str, Any] | None = None
    error: dict[str, Any] | None = None



# ============================================ ENDPOINTS ============================================ #
# =========================================================
# Register user info
# =========================================================
@register_router.post(
    '/me',
    status_code=status.HTTP_201_CREATED,
    summary="App register user",
    description="Register user into database with `payload` provided",
)
def register_user(
    payload: Annotated[RegisterMeRequest, Body(
        examples=[{
            'firstname': 'John',
            'lastname': 'Doe',
            'sexe': 'M',
            'birth': '2000-01-01',
            'email': 'john.doe@gmail.com',
            'country_id': 0
        }]
    )],
    session: Annotated[Session, Depends(get_db_session)],
    content_type: str = Header(..., alias='Content-Type'),
) -> RegisterResponse :
    """ """

    response = RegisterResponse()
    
    if content_type != "application/json" :
        raise RequestHeaderException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            code="UNSUPPORTED_MEDIA_TYPE",
            message="Request media type is not acceptable"
        )

    # 1. Créér le modèle de `UserInfo`
    new_user = UserInfo(**payload.model_dump(), role_id=10)

    try :
        # 2. Insérer dans la BDD
       
        result = new_user.create(session=session)
        response.success = True
        response.response = result

        return response

    except IntegrityError as e:
        session.rollback()
        raise DataBaseException(
            status_code=status.HTTP_409_CONFLICT,
            code="DUPLICATE_ERROR",
            message="The user could not be created because a database constraint was violated."
        ) from None

    except SQLAlchemyError :
        session.rollback()
        raise DataBaseException(
            status_code=status.HTTP_409_CONFLICT,
            code="DATABASE_ERROR",
            message="A database error occurred."
        ) from None


# =========================================================
# Register user account
# =========================================================
@register_router.post(
    '/account',
    status_code=status.HTTP_201_CREATED,
    summary="App register account",
    description="Register user account into database with `payload` provided",
)
def register_account(
    payload: Annotated[RegisterAccountRequest, Body(
        examples=[{
            'user_id': 0,
            'identity': 'john.doe2000',
            'password': 'myPassw0rdIsSiMPle'
        }]
    )],
    session: Annotated[Session, Depends(get_db_session)],
    content_type: str = Header(..., alias='Content-Type'),
) -> RegisterResponse :
    """ """

    response = RegisterResponse()
        
    if content_type != "application/json" :
        raise RequestHeaderException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            code="UNSUPPORTED_MEDIA_TYPE",
            message="Request media type is not acceptable"
        )


    # 1. Vérifier que le profil associé existe.
    if not UserInfo.get_user_by_id(session=session, id=payload.user_id) :
        raise DataBaseException(
            status_code=status.HTTP_404_NOT_FOUND,
            code="MISSING_ERROR",
            message="The profil associated is not found."
        )

    # Créér le profil
    new_user_account = UserAccount(
        user_id=payload.user_id,
        identity=payload.identity,
        password_hashed=hash_password(payload.password)
    )

    try :
        # 2. Insérer dans la BDD
        result = new_user_account.create(session=session)
        response.success = True
        response.response = result

        return response

    except IntegrityError :
        session.rollback()
        
        raise DataBaseException(
            status_code=status.HTTP_409_CONFLICT,
            code="DUPLICATE_ERROR",
            message="The user_id mismatch with identity ."
        ) from None

    except SQLAlchemyError :
        session.rollback()

        raise DataBaseException(
            status_code=status.HTTP_409_CONFLICT,
            code="DATABASE_ERROR",
            message="A database error occurred."
        ) from None

