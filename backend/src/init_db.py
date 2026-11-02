import json
from sqlalchemy.orm import Session

from src.models import Country, UserRole
from src.config import settings



def init_country_db(session: Session) -> None:
    """ """

    with open(settings.PROJECT_JSON_DIR / "countries.json", 'r') as json_file :
        countries = json.load(json_file)

        for country in countries :
            new_country = Country(**country)
            session.add(new_country)
            session.commit()



def init_role_db(session: Session) -> None:
    """ """

    with open(settings.PROJECT_JSON_DIR / "roles.json", 'r') as json_file :
        roles = json.load(json_file)

        for role in roles :
            new_role = UserRole(**role)
            session.add(new_role)
            session.commit()