from typing import Generator
from sqlalchemy import event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from src.config import settings



engine = create_engine(
    url=settings.DB_PATH,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()



class Base(DeclarativeBase) :

    pass



def get_db_session() -> Generator[Session] :

    with SessionLocal() as session :
        yield session