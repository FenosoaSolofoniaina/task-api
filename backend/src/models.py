# ===========================================
# IMPORTS
# ===========================================
import datetime as dt
from typing import Any
from sqlalchemy import String, ForeignKey, DateTime, Date, CheckConstraint, UniqueConstraint, Boolean, Text
from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column, relationship

from src.database import Base


# ===========================================
# USER INFO
# ===========================================
class UserInfo(Base) :

    # ========================= CONFIGURATION =========================
    __tablename__= "users"

    __table_args__ = (
        CheckConstraint(
            "sexe IN ('M', 'F')",
            name="check_user_sexe",
        ),
        UniqueConstraint(
            "firstname",
            "lastname",
            "sexe",
            "birth",
            "country_id",
            "email",
            name="check_unique_user"
        )
    )

    # ========================= COLUMNS =========================
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    lastname: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    sexe: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )
    birth: Mapped[dt.date] = mapped_column(
        Date,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.datetime.now(tz=dt.timezone.utc)
    )
    country_id: Mapped[int] = mapped_column(
        ForeignKey('countries.id'),
        nullable=False
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey('roles.id'),
        default=10,
        nullable=False
    )

    # ========================= RELATIONS =========================
    country: Mapped["Country"] = relationship(
        "Country",
        uselist=False,
        back_populates="users"
    )
    account: Mapped["UserAccount | None"] = relationship(
        "UserAccount",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    role: Mapped["UserRole"] = relationship(
        "UserRole",
        uselist=False,
        back_populates="users"
    )
    session: Mapped["UserSession | None"] = relationship(
            "UserSession",
            back_populates="user",
            uselist=False,
            cascade="all, delete-orphan"
        )
    tasks: Mapped[list["TaskData"]] = relationship(
        "TaskData",
        uselist=True,
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    # ========================= METHODS =========================
    def create_user(self, session: Session) -> dict[str, Any] :
        """ """
        
        session.add(self)
        session.commit()
        session.refresh(self)

        return {
            'user_id': self.id,
            'created_at': self.created_at.isoformat()
        }
        
    
    @classmethod
    def get_user_by_id(cls: "UserInfo",
                       session: Session,
                       id: int) -> "UserInfo | None" :
        """ """

        return session.get(cls, id)



# ===========================================
# USER ACCOUNT
# ===========================================
class UserAccount(Base) :

    # ========================= CONFIGURATION =========================
    __tablename__= "user_accounts"

    # ========================= COLUMNS =========================
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete="CASCADE"),
        primary_key=True
    )
    identity: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )
    password_hashed: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    last_log: Mapped[dt.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=dt.datetime.now
    )
    

    # ========================= RELATIONS =========================
    user: Mapped["UserInfo"] = relationship(
        "UserInfo",
        uselist=False,
        back_populates="account"
    )

    # ========================= METHODS =========================
    def create_account(self, session: Session) -> dict[str, Any] :
        """ """
        
        session.add(self)
        session.commit()
        session.refresh(self)

        return {
            'uid': self.user_id,
            'identity': self.identity,
            'type': 'user',
            'status': 'created'
        }
    

    @classmethod
    def get_account_by_identity(cls: "UserAccount",
                                session: Session,
                                identity: str) -> "UserAccount | None" :

        return session.scalar(
            select(UserAccount).where(UserAccount.identity == identity)
        )



# ===========================================
# SESSION
# ===========================================
class UserSession(Base) :

    # ========================= CONFIGURATION =========================
    __tablename__ = "sessions"

    # ========================= COLUMNS =========================
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    access_token: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.datetime.now(tz=dt.timezone.utc)
    )

    # ========================= RELATIONS =========================
    user: Mapped["UserInfo"] = relationship(
            "UserInfo",
            uselist=False,
            back_populates="session"
        )
    
    # ========================= METHODS =========================
    def create_session(self, session:Session) -> None :
        """ """

        session.add(self)
        session.commit()
        session.refresh(self)
    


    # ========================= RELATIONS =========================
    def remove_session(self, session: Session) -> dict[str, Any] :
        
        """ """
    
        session.delete(self)
        session.commit()

        return {
            'uid': self.id,
            'message': "Session closed and removed"
        }


    @classmethod
    def get_session_by_user_id(cls,
                               session: Session,
                               user_id: int) -> "UserSession" :

        return session.scalar(
            select(UserSession).where(UserSession.user_id == user_id)
        )



# ===========================================
# COUNTRY
# ===========================================
class Country(Base) :

    # ========================= CONFIGURATION =========================
    __tablename__ = "countries"

    # ========================= COLUMNS =========================
    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    abbr: Mapped[str] = mapped_column(
        String(3),
        unique=True,
        nullable=False,
    )

    # ========================= RELATIONS =========================
    users: Mapped[list["UserInfo"]] = relationship(
        "UserInfo",
        back_populates="country"
    )

    # ========================= METHODS =========================
    @classmethod
    def get_country_by_id(cls: "Country",
                          session: Session,
                          id: int) -> "Country | None":
        """ """

        return session.get(cls, id)


    @classmethod
    def get_all_countries(cls: "Country",
                      session: Session) -> list["Country"]:
        """ """

        return list(
            session.scalars(
                select(cls).order_by(cls.name)
            ).all()
        )



# ===========================================
# USER ROLE
# ===========================================
class UserRole(Base) :

    # ========================= CONFIGURATION =========================
    __tablename__ = "roles"

    __table_args__ = (
            CheckConstraint(
                "type IN ('user', 'superuser', 'admin')",
                name="check_user_role_type",
            ),
        )

    # ========================= COLUMNS =========================
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(
        String(10),
        default="user",
        nullable=False,
    )

    # ========================= RELATIONS =========================
    users: Mapped[list["UserInfo"]] = relationship(
        "UserInfo",
        back_populates="role"
    )

    # ========================= METHODS =========================
    @classmethod
    def get_role_by_id(cls: "UserRole",
                       session: Session, 
                       id: int) -> "UserRole | None":
        """ """

        return session.get(cls, id)



# ===========================================
# TASK INFO
# ===========================================
class TaskData(Base) :
    """ """

    # ========================= CONFIGURATIONS =========================
    __tablename__ = "tasks"

    # ========================= COLUMNS =========================
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # ========================= RELATIONS =========================
    owner: Mapped["UserInfo"] = relationship(
        "UserInfo",
        back_populates="tasks",
        uselist=False,
    )