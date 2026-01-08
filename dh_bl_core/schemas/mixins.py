"""Модуль с миксинами для схемы данных."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UuidMixin(BaseModel):
    """
    Миксин схемы данных, добавляющий поле uuid.

    Attributes:
        uuid (UUID): Уникальный идентификатор объекта.

    Example:
        >>> from uuid import uuid4
        >>> from dh_bl_core.schemas import UuidMixin
        >>>
        >>> class User(UuidMixin):
        >>>     name: str
        >>>
        >>> user = User(uuid=uuid4(), name="John")
        >>> print(user.uuid)
        # UUID('...')
    """

    uuid: UUID


class TimestampMixin(BaseModel):
    """
    Миксин схемы данных, добавляющий поля временных меток.

    Attributes:
        created_at (datetime): Время создания объекта.
        updated_at (datetime): Время последнего обновления объекта.
        is_created (bool): Флаг, указывающий, был ли объект создан.

    Example:
        >>> from dh_bl_core.schemas import TimestampMixin
        >>>
        >>> class User(TimestampMixin):
        >>>     name: str
        >>>
        >>> user = User(created_at=datetime.now(), updated_at=datetime.now(), name="John")
        >>> print(user.created_at)
        # 2026-01-01 12:00:00.000000
        >>> print(user.updated_at)
        # 2026-01-01 12:00:00.000000
        >>> print(user.is_created)
        # True
        >>> # Изменение времени обновления, чтобы имитировать обновление объекта.
        >>> # Такой объект уже не считается созданным, а измененным
        >>> user.updated_at = datetime.now()
        >>> print(user.is_created)
        # False
    """

    created_at: datetime
    updated_at: datetime
    is_created: bool


class DeleteMixin(BaseModel):
    """
    Миксин схемы данных, добавляющий поля для мягкого удаления.

    Attributes:
        deleted_at (datetime | None): Время удаления объекта или None, если не удалён.
        is_deleted (bool): Флаг, указывающий, был ли объект удалён.

    Example:
        >>> from dh_bl_core.schemas import DeleteMixin
        >>>
        >>> class User(DeleteMixin):
        >>>     name: str
        >>>
        >>> user = User(name="John")
        >>> print(user.is_deleted)
        >>> # Устанавливаем дату удаления
        >>> user.deleted_at = datetime.now()
        >>> print(user.is_deleted)
        # True
    """

    deleted_at: datetime | None
    is_deleted: bool


class DeactivateMixin(BaseModel):
    """
    Миксин схемы данных, добавляющий поля для деактивации объекта.

    Attributes:
        deactivated_at (datetime | None): Время деактивации объекта или None, если активен.
        is_deactivated (bool): Флаг, указывающий, был ли объект деактивирован.

    Example:
        >>> from dh_bl_core.schemas import DeactivateMixin
        >>>
        >>> class User(DeactivateMixin):
        >>>     name: str
        >>>
        >>> user = User(name="John")
        >>> print(user.is_deactivated)
        >>> # Устанавливаем дату деактивации
        >>> user.deactivated_at = datetime.now()
        >>> print(user.is_deactivated)
        # True
    """

    deactivated_at: datetime | None
    is_deactivated: bool
