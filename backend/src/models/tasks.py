# ===========================================
# TASK INFO
# ===========================================
import uuid
import datetime as dt
from typing import TYPE_CHECKING
from sqlalchemy import Text, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship


from src.database import Base
if TYPE_CHECKING :
    from .accounts import UserInfo


# ===========================================
# TASK INFO
# ===========================================
class TaskData(Base) :
    """ """

    # ========================= CONFIGURATIONS =========================
    __tablename__ = "tasks"

    # ========================= COLUMNS =========================
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    completed_at: Mapped[dt.datetime] = mapped_column(
        DateTime,
        nullable=True,
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