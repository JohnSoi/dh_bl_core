"""Модуль с зависимостями для работы с базой данных."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .manager import db_manager


async def get_db() -> AsyncGenerator[AsyncSession | Session, None]:
    """
    Возвращает сессию базы данных для использования в качестве зависимости.

    Предоставляет асинхронную сессию SQLAlchemy, которая автоматически
    управляется через контекстный менеджер: открывается в начале и закрывается
    в блоке finally. Подходит для операций чтения и записи, где коммит
    необходимо выполнять вручную.

    Откат транзакции (rollback) выполняется автоматически при возникновении исключений.

    Returns:
        AsyncSession | Session: Активная сессия базы данных.

    Examples:
        >>> from fastapi import Depends
        >>> from dh_bl_core.database import BaseModel
        >>> class User(BaseModel):
        ...     pass
        >>>
        >>> async def get_user(user_id: int, db: Session = Depends(get_db)):
        ...     return await db.get(User, user_id)
        ...
        >>> async def main() -> None:
        ...     user = await get_user(123)

    Notes:
        Не выполняет коммит автоматически — вызовите db.commit() вручную при необходимости.
    """
    async with db_manager.session_maker() as async_session:
        try:
            yield async_session
        except Exception:
            await async_session.rollback()
            raise
        finally:
            await async_session.close()
