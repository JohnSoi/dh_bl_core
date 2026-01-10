"""Базовый сервис."""
from typing import Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import EmptyRepositoryNotAllowedException
from .types import BaseRepository


class BaseService(Generic[BaseRepository]):
    _REPOSITORY: Type[BaseRepository]

    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session
        self._repository = self._REPOSITORY(db_session)

        if not self._repository:
            raise EmptyRepositoryNotAllowedException()
