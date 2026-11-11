import json
import datetime as dt
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from src.models import Country, UserRole, UserInfo, UserAccount, TaskData
from src.config import settings
from src.database import engine, Base



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



def init_user_info_db(session: Session) -> None:
    """ """

    new_user = UserInfo(
        id=1,
        firstname="John",
        lastname="Doe",
        sexe="M",
        birth=dt.date(year=2000, month=1, day=1),
        email="john.doe@gmail.com",
        country_id=1
    )
    session.add(new_user)
    session.commit()



def init_user_account_db(session: Session) -> None:
    """ """

    new_account = UserAccount(
        user_id=1,
        identity="john.doe",
        password_hashed=PasswordHash.recommended().hash("johnDoe1")
    )
    session.add(new_account)
    session.commit()



def init_task_db(session: Session) -> None:
    """ """

    new_task = TaskData(
        title="Eat",
        description="Eat some fruits and vegetables",
        created_at=dt.datetime.now(tz=dt.timezone.utc),
        completed=False,
        owner_id=1
    )
    session.add(new_task)
    session.commit()
    
    
    
def initialize_database(session: Session) -> None :
    """ """

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    init_country_db(session=session)
    init_role_db(session=session)
    init_user_info_db(session=session)
    init_user_account_db(session=session)
    init_task_db(session=session)