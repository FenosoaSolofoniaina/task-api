from typing import Any, Annotated
from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.models import Country
from src.utilities.database import get_db_session



# ============================================ ROUTER ============================================ #
utils_router = APIRouter(
    prefix='/utils',
    tags=['Utils']
)


# ============================================ SCHEMAS ============================================ #
# ================================================================================ #
# List of countries
# ================================================================================ #
class SingleCountryResponse(BaseModel) :
    """ """

    id: int
    name: str
    abbr: str



class CountryListResponse(BaseModel) :
    """ """

    success: bool = False
    response: list[SingleCountryResponse | None] = []
    error: dict[str, Any] | None = None


# ============================================ ENDPOINTS ============================================ #
# =========================================================
# GET ALL COUNTRIES
# =========================================================
@utils_router.get(
    '/countries',
    summary="/Get list of countries",
    description="Get list of countries inside /jsons/countries.json",
)
def get_countries(
    session: Annotated[Session, Depends(get_db_session)]
) -> CountryListResponse:
    
    """ """

    all_countries = Country.get_all_countries(session=session)

    return CountryListResponse(
        success=True,
        response=[SingleCountryResponse(id=country.id, name=country.name, abbr=country.abbr) for country in all_countries]
    )