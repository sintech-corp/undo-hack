import datetime
import uuid

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin(object):
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class UpdatedAtMixin(object):
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class UidMixin(object):
    uid: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=lambda: uuid.uuid4())


class BaseDBModel(CreatedAtMixin, UpdatedAtMixin, UidMixin):
    pass
