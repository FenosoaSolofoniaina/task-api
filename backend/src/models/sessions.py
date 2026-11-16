# ===========================================
# IMPORTS
# ===========================================
import uuid
import datetime as dt
from typing import Any, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, DateTime, Boolean
from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column, relationship


from src.database import Base
if TYPE_CHECKING :
    from .accounts import UserAccount



# ===========================================
# SESSION
# ===========================================
class UserSession(Base) :

    # ========================= CONFIGURATION =========================
    __tablename__ = "sessions"


    # ========================= COLUMNS =========================
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user_accounts.user_id', ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    access_token: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        unique=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.datetime.now(tz=dt.timezone.utc)
    )
    revoked_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ========================= RELATIONS =========================
    account: Mapped["UserAccount"] = relationship(
        "UserAccount",
        uselist=False,
        back_populates="session"
    )
    
    # ========================= METHODS =========================
    def create(self, session: Session) -> dict[str, Any] :
        """ """

        session.add(self)
        session.commit()
        session.refresh(self)

        return {
            'sid': self.id,
            'createdAt': self.created_at
        }


    def revoke(self, session: Session) -> dict[str, Any] :
        """ """

        self.revoked = True
        self.revoked_at = dt.datetime.now(tz=dt.timezone.utc)
        session.commit()
        session.refresh(self)

        return {
            'sid': self.id,
            'revoked': True
        }


    @classmethod
    def revoke_session_by_token(cls,
                             session: Session,
                             token: str) -> dict[str, Any] :
        """ """

        current_session = session.scalar(
            select(UserSession).where(UserSession.access_token == token)
        )

        return current_session.revoke()


    @classmethod
    def get_active_session(cls,
                           session: Session,
                           user_id: int) -> "UserSession" :
        """ """

        current_session = session.scalar(
            select(UserSession).where(UserSession.user_id == user_id,
                                      UserSession.revoked == False)
        )

        return current_session