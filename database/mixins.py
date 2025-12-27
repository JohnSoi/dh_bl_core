from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy import UUID as PG_UUID, Column, text, DateTime, func


class UuidMixin:
    uuid: Mapped[UUID] = Column(PG_UUID(as_uuid=True), server_default=text("gen_random_uuid()"), nullable=False)


class TimestampMixin:
    created_at: Mapped[datetime] = Column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    @property
    def is_created(self) -> bool:
        return self.created_at == self.updated_at


class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = Column(DateTime)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


class DeactivateMixin:
    deactivated_at: Mapped[datetime | None] = Column(DateTime)

    @property
    def is_deactivated(self) -> bool:
        return self.deactivated_at is not None
