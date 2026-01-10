# pylint: disable=too-few-public-methods
"""Базовый сервис."""

from typing import Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import EmptyRepositoryNotAllowedException
from .types import BaseRepository


class BaseService(Generic[BaseRepository]):
    """
    Базовый сервис для всех сервисов приложения.

    Предоставляет базовую функциональность для сервисов, включая управление сессией базы данных
    и инициализацию репозитория. Является обобщённым классом, который должен быть унаследован
    конкретными сервисами.

    Attributes:
        _REPOSITORY (Type[BaseRepository]): Тип репозитория, который будет использоваться
            в наследующем классе. Должен быть определён в подклассе.
        _db_session (AsyncSession): Асинхронная сессия базы данных.
        _repository (BaseRepository): Экземпляр репозитория, инициализированный с сессией БД.

    Examples:
        >>> from sqlalchemy.ext.asyncio import AsyncSession
        >>> from dh_bl_core.service.types import BaseRepository
        >>>
        >>> class MyRepository(BaseRepository):
        ...     def __init__(self, db_session: AsyncSession) -> None:
        ...         self._db_session = db_session
        ...
        >>> class MyService(BaseService[MyRepository]):
        ...     _REPOSITORY = MyRepository
        ...
        >>> # Создание сервиса с сессией
        >>> db_session = AsyncSession()
        >>> service = MyService(db_session)
        >>> isinstance(service._repository, MyRepository)
        True
        >>> service._db_session is db_session
        True
    """

    _REPOSITORY: Type[BaseRepository]

    def __init__(self, db_session: AsyncSession) -> None:
        """
        Инициализирует базовый сервис с асинхронной сессией базы данных.

        Создаёт экземпляр репозитория, указанного в атрибуте _REPOSITORY, и передаёт ему
        сессию базы данных. Если репозиторий не может быть создан (равен None),
        выбрасывается исключение.

        Args:
            db_session (AsyncSession): Асинхронная сессия базы данных для работы с репозиторием.

        Raises:
            EmptyRepositoryNotAllowedException: Если репозиторий не был создан
                (равен None), что указывает на некорректную конфигурацию сервиса.

        Examples:
            >>> from sqlalchemy.ext.asyncio import AsyncSession
            >>>
            >>> # Инициализация сервиса с сессией
            >>> db_session = AsyncSession()
            >>> service = MyService(db_session)
            >>> service._db_session is db_session
            True
            >>>
            >>> # Попытка инициализации с некорректным репозиторием
            >>> class InvalidService(BaseService[MyRepository]):
            ...     pass  # _REPOSITORY не определён
            ...
            >>> service = InvalidService(db_session)  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            dh_bl_core.service.exceptions.EmptyRepositoryNotAllowedException: Репозиторий не может быть пустым.
        """
        self._db_session = db_session
        self._repository = self._REPOSITORY(db_session)

        if not self._repository:
            raise EmptyRepositoryNotAllowedException()
