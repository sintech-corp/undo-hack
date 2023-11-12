import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Table, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
from models.mixins import BaseDBModel, CreatedAtMixin, UpdatedAtMixin


if TYPE_CHECKING:
    from models.compensation_requests import CompensationRequestGrade


class User(BaseDBModel, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone_number: Mapped[str]

    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str | None]

    is_active: Mapped[bool] = mapped_column(default=True)
    is_staff: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    position: Mapped[str | None]

    hashed_password: Mapped[str]
    last_login_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )

    grades: Mapped[list["CompensationRequestGrade"]] = relationship(back_populates="author")