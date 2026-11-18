# ===========================================
# IMPORTS
# ===========================================
import datetime as dt
from typing import Any, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, DateTime, Date, CheckConstraint, UniqueConstraint
from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column, relationship


from src.utilities.database import Base
if TYPE_CHECKING :
    from .sessions import UserSession
    from .tasks import TaskData


    
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
        unique=True,
        index=True,
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
    tasks: Mapped[list["TaskData"]] = relationship(
        "TaskData",
        uselist=True,
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    # ========================= METHODS =========================
    def create(self, session: Session) -> dict[str, Any] :
        """ """
        
        session.add(self)
        session.commit()
        session.refresh(self)

        return {
            'user_id': self.id,
            'created_at': self.created_at.isoformat()
        }
        
    
    @classmethod
    def get_user_by_id(cls,
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
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True,
    )
    identity: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    password_hashed: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    
    # ========================= RELATIONS =========================
    user: Mapped["UserInfo"] = relationship(
        "UserInfo",
        uselist=False,
        back_populates="account"
    )
    session: Mapped["UserSession"] = relationship(
        "UserSession",
        uselist=False,
        back_populates="account"
    )

    # ========================= METHODS =========================
    def create(self, session: Session) -> dict[str, Any] :
        """ """
        
        session.add(self)
        session.commit()
        session.refresh(self)

        return {
            'uid': self.user_id,
            'identity': self.identity,
            'status': 'created'
        }
    

    @classmethod
    def get_account_by_identity(cls,
                                session: Session,
                                identity: str) -> "UserAccount | None" :

        return session.scalar(
            select(UserAccount).where(UserAccount.identity == identity)
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
    def get_country_by_id(cls,
                          session: Session,
                          id: int) -> "Country | None":
        """ """

        return session.get(cls, id)


    @classmethod
    def get_all_countries(cls,
                          session: Session) -> list["Country"]:
        """ """

        return list(session.scalars(select(cls)).all())


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
    def get_role_by_id(cls,
                       session: Session, 
                       id: int) -> "UserRole | None":
        """ """

        return session.get(cls, id)