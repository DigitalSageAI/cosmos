from typing import Optional, Annotated

from sqlalchemy import Column, Integer, BigInteger, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from tg_bot.db.session import Base



intpk = Annotated[int, mapped_column(primary_key=True)]



class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    tg_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    lang: Mapped[str] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False, default=True)
    utm: Mapped[Optional[str]] = mapped_column(ForeignKey("utm_info.utm"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.now
    )


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[intpk]
    tg_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("users.tg_id"), nullable=False)
    notification_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    notification_type: Mapped[Optional[str]] = mapped_column(nullable=False)
    job_id: Mapped[str | None] = mapped_column(nullable=True)


class UTMInfo(Base):
    __tablename__ = "utm_info"

    id: Mapped[intpk]
    utm: Mapped[str] = mapped_column(nullable=False, unique=True)
    source: Mapped[str] = mapped_column(nullable=False)
    info: Mapped[Optional[str]] = mapped_column(nullable=True)