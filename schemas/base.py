"""Базовый класс для схем данных."""
from pydantic import BaseModel


class BaseSchema(BaseModel):
    """
    Базовая схема данных приложения.

    Notes:
        Все схемы данных должны наследоваться от этого класса.

    Attributes:
        id (int): Уникальный идентификатор объекта.

    Example:
        >>> from dh_bl_core.schemas import BaseSchema
        >>>
        >>> class User(BaseSchema):
        >>>     name: str
        >>>
        >>> user = User(id=1, name="John")
        >>> print(user.id)
        # 1
    """
    id: int
