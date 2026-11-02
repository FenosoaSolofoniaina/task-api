# ===========================================
# IMPORTS
# ===========================================
import datetime as dt
from typing import Any
from sqlalchemy import String, ForeignKey, DateTime, Date, CheckConstraint, UniqueConstraint, Boolean
from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.database import Base
from src.jwt_token import encode_token


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

    # ========================= METHODS =========================
    def create_user(self, session: Session) -> dict[str, Any] :
        """ """

        try :
            session.add(self)
            session.commit()
            session.refresh(self)

            return {
                'user_id': self.id,
                'created_at': self.created_at.isoformat()
            }
        
        except IntegrityError :
            session.rollback()
            raise

        except SQLAlchemyError :
            session.rollback()
    
    
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
    last_log: Mapped[dt.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=dt.datetime.now
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
    

    # ========================= RELATIONS =========================
    user: Mapped["UserInfo"] = relationship(
        "UserInfo",
        uselist=False,
        back_populates="account"
    )
    session: Mapped["UserSession | None"] = relationship(
        "UserSession",
        uselist=False,
        back_populates="account",
        cascade="all, delete-orphan"
    )

    # ========================= METHODS =========================
    def create_account(self, session: Session) -> dict :
        """ """

        try :
            session.add(self)
            session.commit()
            session.refresh(self)

            return {
                'uid': self.user_id,
                'identity': self.identity,
                'type': 'user',
                'status': 'created'
            }
        
        except IntegrityError :
            session.rollback()
            raise

        except SQLAlchemyError :
            session.rollback()
            raise


    @classmethod
    def get_user_by_identity(cls: "UserAccount",
                             session: Session,
                             identity: str) -> "UserAccount | None" :

        return session.scalar(
            select(UserAccount).where(UserAccount.identity == identity)
        )
    

    @classmethod
    def get_identity(cls: "UserAccount",
                    session: Session,
                    user_id: int) -> str :
        """ """

        return session.scalar(
            select(UserAccount.identity).where(UserAccount.user_id == user_id)
        )



# ===========================================
# SESSION
# ===========================================
class UserSession(Base) :

    # ========================= CONFIGURATION =========================
    __tablename__ = "sessions"

    # ========================= COLUMNS =========================
    id: Mapped[int] = mapped_column(primary_key=True)
    account_user_id: Mapped[int] = mapped_column(
        ForeignKey('user_accounts.user_id', ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=dt.datetime.now
    )
    access_token: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )
    refresh_token: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )
    token_type: Mapped[str] = mapped_column(
        String(10),
        default='bearer',
        nullable=False
    )
    revoked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    # ========================= RELATIONS =========================
    account: Mapped["UserAccount"] = relationship(
        "UserAccount",
        uselist=False,
        back_populates="session"
    )

    # ========================= RELATIONS =========================
    @classmethod
    def create_session(cls: "UserSession",
                       session:Session,
                       account: "UserAccount") -> "UserSession" :
        """ """

        access_token = encode_token(account, token_type='access')
        refresh_token = encode_token(account, token_type='refresh')

        new_session = cls(
            account_user_id=account.user_id,
            access_token=access_token,
            refresh_token=refresh_token
        )

        try :
            session.add(new_session)
            session.commit()
            session.refresh(new_session)

            return new_session

        except IntegrityError :
            session.rollback()
            raise

        except SQLAlchemyError :
            session.rollback()
            raise



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