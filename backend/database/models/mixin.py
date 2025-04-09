from datetime import date, datetime

from sqlalchemy import Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class CreationDateMixin:
    creation_date: Mapped[date] = mapped_column(
        Date(), server_default=func.current_date()
    )


class TimestampMixin:
    """Миксин для отслеживания времени создания и обновления записи"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class IsActiveMixin:
    """Миксин для soft delete"""

    is_active: Mapped[bool] = mapped_column(default=True)
