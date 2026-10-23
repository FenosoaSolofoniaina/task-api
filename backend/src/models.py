from datetime import date
from sqlalchemy import String, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Country(Base) :

    __tablename__ = "countries"

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

    users: Mapped[list["UserInfo"]] = relationship(back_populates="country")


class UserIdentity(Base) :

    __tablename__= "users_identity"

    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
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

    user: Mapped["UserInfo"] = relationship(back_populates="identity")


class UserInfo(Base) :

    __tablename__= "users"

    __table_args__ = (
        CheckConstraint(
            "sexe IN ('M', 'F')",
            name="check_user_sexe",
        ),
    )

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
    birth: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'))

    country: Mapped["Country"] = relationship(back_populates="users")
    identity: Mapped["UserIdentity"] = relationship(back_populates="user")