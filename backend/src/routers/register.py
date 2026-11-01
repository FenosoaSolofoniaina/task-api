import datetime as dt
from typing import Annotated
from fastapi import APIRouter
from fastapi import Body, Header
from fastapi import status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pwdlib import PasswordHash

from src.database import SessionLocal
from src.models import UserInfo, UserAccount
from src.schemas import RegisterMeDataInput, RegisterDataOutput, RegisterAccountInput
from src.exceptions import DataBaseException, RequestHeaderException



password_hasher = PasswordHash.recommended()

# ============================================ ROUTER ============================================ #
register_router = APIRouter(
    prefix='/register',
    tags=['Register']
)

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
    payload: Annotated[
        RegisterMeDataInput,
        Body(examples=[{'firstname': 'John','lastname': 'Doe','sexe': 'M','birth': '2000-01-01','country_id': 0}])
    ],
    content_type: str = Header(..., alias='Content-Type'),
) -> RegisterDataOutput :
    """ """

    response = RegisterDataOutput()
    
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
        with SessionLocal() as session :
            result = new_user.create_user(session=session)
            response.success = True
            response.response = result

        return response

    except IntegrityError as e:
        print(e.orig)
        raise DataBaseException(
            status_code=status.HTTP_409_CONFLICT,
            code="DUPLICATE_ERROR",
            message="The user could not be created because a database constraint was violated."
        ) from None

    except SQLAlchemyError :
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
    payload: Annotated[
        RegisterAccountInput,
        Body(examples=[{'user_id': 0,'identity': 'john.doe2000','password': 'myPassw0rdIsSiMPle',}])
    ],
    content_type: str = Header(..., alias='Content-Type'),
) -> RegisterDataOutput :
    """ """

    response = RegisterDataOutput()
        
    if content_type != "application/json" :
        raise RequestHeaderException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            code="UNSUPPORTED_MEDIA_TYPE",
            message="Request media type is not acceptable"
        )

    with SessionLocal() as session :

        # 1. Vérifier que le profil associé existe.
        if not UserInfo.get_user_by_id(session=session, id=payload.user_id) :
            raise DataBaseException(
                status_code=status.HTTP_404_NOT_FOUND,
                code="MISSING_ERROR",
                message="The profil associated is not found."
            )
        
        new_user_account = UserAccount(
            user_id=payload.user_id,
            identity=payload.identity,
            password_hashed=password_hasher.hash(payload.password),
            last_log=dt.date.today()
        )

        try :
            # 2. Insérer dans la BDD
            result = new_user_account.create_account(session=session)
            response.success = True
            response.response = result
    
            return response
    
        except IntegrityError :
            raise DataBaseException(
                status_code=status.HTTP_409_CONFLICT,
                code="DUPLICATE_ERROR",
                message="The identity already exist."
            ) from None
    
        except SQLAlchemyError :
            raise DataBaseException(
                status_code=status.HTTP_409_CONFLICT,
                code="DATABASE_ERROR",
                message="A database error occurred."
            ) from None

