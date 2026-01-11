"""Базовый сервис."""

from typing import Generic, Type
from uuid import UUID

from pydantic import BaseModel as BaseSchema
from sqlalchemy.ext.asyncio import AsyncSession

from dh_bl_core.database.types import BaseModel
from dh_bl_core.logging import LogManager

from .exceptions import EmptyRepositoryNotAllowedException
from .types import BaseRepository


class BaseService(Generic[BaseRepository, BaseModel]):
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
        >>> from dh_bl_core.database import BaseRepository
        >>>
        >>> class MyRepository(BaseRepository):
        ...     ...
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
    _LOGGER = LogManager().logger

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
            >>> from dh_bl_core.service import BaseService
            >>> from dh_bl_core.database import BaseRepository
            >>>
            >>> class MyRepository(BaseRepository):
            ...     ...
            >>>
            >>> class MyService(BaseService):
            ...     ...
            ...
            >>> # Инициализация сервиса с сессией
            >>> db_session_instance = AsyncSession()
            >>> service = MyService(db_session_instance)
            >>> service._db_session is db_session_instance
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
            self._LOGGER.error("Репозиторий не может быть пустым.")
            raise EmptyRepositoryNotAllowedException()

        self._LOGGER.debug(f'Сервис "{self.__class__.__name__}" инициализирован.')

    async def create(self, payload: BaseSchema) -> BaseModel:
        """
        Создаёт новую сущность в базе данных.

        Метод принимает объект схемы Pydantic, преобразует его в словарь
        (исключая неустановленные поля) и передаёт репозиторию для создания записи.

        Args:
            payload (BaseSchema): Объект схемы Pydantic с данными для создания сущности.

        Returns:
            BaseModel: Созданная сущность в виде модели базы данных.

        Examples:
            >>> from dh_bl_core.database import BaseModel
            >>>
            >>> class UserCreateSchema(BaseSchema):
            ...     name: str
            ...     email: str
            ...
            >>> class UserModel(BaseModel):
            ...     id: int
            ...     name: str
            ...     email: str
            ...
            >>> # Мок для репозитория
            >>> class MockRepository:
            ...     async def create(self, data: dict):
            ...         return UserModel(id=1, **data)
            ...
            >>> class MyService(BaseService):
            ...     ...
            ...
            >>> # Инициализация сервиса с сессией
            >>> db_session_instance = AsyncSession()
            >>> # Создание сервиса с моком репозитория
            >>> service = MyService(db_session_instance)
            >>> service._repository = MockRepository()
            >>>
            >>> async def main():
            ...     # Создание новой сущности
            ...     user_payload = UserCreateSchema(name="John", email="john@example.com")
            ...     result: UserModel = await service.create(user_payload)
            ...     # True
            ...     isinstance(result, UserModel)
            ...     print(result.name)
            'John'
        """
        self._LOGGER.debug(f'Создание сущности "{payload.__class__.__name__}" в сервисе "{self.__class__.__name__}".')
        return await self._repository.create(payload.model_dump(exclude_unset=True))

    async def update(self, payload: BaseSchema) -> BaseModel:
        """
        Обновляет существующую сущность в базе данных.

        Метод принимает объект схемы Pydantic, преобразует его в словарь
        (исключая неустановленные поля) и передаёт репозиторию для обновления записи.

        Args:
            payload (BaseSchema): Объект схемы Pydantic с данными для обновления сущности.
                Должен включать идентификатор обновляемой сущности.

        Returns:
            BaseModel: Обновлённая сущность в виде модели базы данных.

        Examples:
            >>> from dh_bl_core.database import BaseModel
            >>>
            >>> class UserUpdateSchema(BaseSchema):
            ...     id: int
            ...     name: str
            ...
            >>> class UserModel(BaseModel):
            ...     id: int
            ...     name: str
            ...     email: str
            ...
            >>> # Мок для репозитория
            >>> class MockRepository:
            ...     async def update(self, data: dict):
            ...         return UserModel(id=data["id"], name=data["name"], email="old@example.com")
            ...
            >>> # Создание сервиса с моком репозитория
            >>> class MyService(BaseService):
            ...     ...
            ...
            >>> # Инициализация сервиса с сессией
            >>> db_session_instance = AsyncSession()
            >>> service = MyService(db_session_instance)
            >>> service._repository = MockRepository()
            >>>
            >>> async def main():
            ...     # Обновление сущности
            ...     user_payload = UserUpdateSchema(id=1, name="John Doe")
            ...     result: UserModel = await service.update(payload)
            ...     # True
            ...     isinstance(result, UserModel)
            ...     print(result.name)
            'John Doe'
        """
        self._LOGGER.debug(f'Обновление сущности "{payload.__class__.__name__}" в сервисе "{self.__class__.__name__}".')
        return await self._repository.update(payload.model_dump(exclude_unset=True))

    async def delete(self, entity_id: int) -> bool:
        """
        Удаляет сущность из базы данных.

        Метод принимает объект схемы Pydantic, преобразует его в словарь
        (исключая неустановленные поля) и передаёт репозиторию для удаления записи.

        Args:
            entity_id (int): Идентификатор удаляемой сущности.

        Returns:
            bool: True, если сущность была успешно удалена, иначе False.

        Examples:
            >>> # Мок для репозитория
            >>> class MockRepository:
            ...     async def delete(self, data: dict) -> bool:
            ...         return True
            ...
            >>> # Создание сервиса с моком репозитория
            >>> class MyService(BaseService):
            ...     ...
            ...
            >>> # Инициализация сервиса с сессией
            >>> db_session_instance = AsyncSession()
            >>> service = MyService(db_session_instance)
            >>> service._repository = MockRepository()
            >>>
            >>> async def main():
            ...     # Удаление сущности
            ...     result = await service.delete(1)
            ...     print(result)
            True
        """
        self._LOGGER.debug(f'Удаление сущности с ID "{entity_id}" в сервисе "{self.__class__.__name__}".')
        return await self._repository.delete(entity_id)

    async def get(self, entity_id: int) -> BaseModel:
        """
        Получает сущность по её идентификатору.

        Метод передаёт идентификатор репозиторию для получения соответствующей записи
        из базы данных.

        Args:
            entity_id (int): Идентификатор сущности, которую нужно получить.

        Returns:
            BaseModel: Найденная сущность в виде модели базы данных.

        Examples:
            >>> from dh_bl_core.database import BaseModel
            >>>
            >>> class UserModel(BaseModel):
            ...     id: int
            ...     name: str
            ...     email: str
            ...
            >>> # Мок для репозитория
            >>> class MockRepository:
            ...     async def get(self, entity_id: int):
            ...         if entity_id == 1:
            ...             return UserModel(id=1, name="John", email="john@example.com")
            ...         return None
            ...
            >>> # Создание сервиса с моком репозитория
            >>> class MyService(BaseService):
            ...     ...
            ...
            >>> # Инициализация сервиса с сессией
            >>> db_session_instance = AsyncSession()
            >>> service = MyService(db_session_instance)
            >>> service._repository = MockRepository()
            >>>
            >>> async def main():
            ...     # Получение существующей сущности
            ...     result: UserModel = await service.get(1)
            ...     print(isinstance(result, UserModel))
            ...     # True
            ...     print(result.name)
            ...     # 'John'
            ...
            ...     # Получение несуществующей сущности (возвращается None)
            ...     result = await service.get(999)
            ...     print(result is None)
            ...     # True
        """
        self._LOGGER.debug(f'Получение сущности с ID "{entity_id}" в сервисе "{self.__class__.__name__}".')
        return await self._repository.get(entity_id)
    
    async def get_by_uuid(self, uuid: UUID) -> BaseModel:
        """
        Получает сущность по её UUID.

        Метод передаёт UUID репозиторию для получения соответствующей записи
        из базы данных.

        Args:
            uuid (UUID): UUID сущности, которую нужно получить.

        Returns:
            BaseModel: Найденная сущность в виде модели базы данных.

        Examples:
            >>> from uuid import UUID
            >>> from dh_bl_core.database import BaseModel
            >>>
            >>> class UserModel(BaseModel):
            ...     id: int
            ...     uuid: UUID
            ...     name: str
            ...     email: str
            ...
            >>> # Мок для репозитория
            >>> class MockRepository:
            ...     async def get_by_uuid(self, uuid: UUID):
            ...         if str(uuid) == "123e4567-e89b-12d3-a456-426614174000":
            ...             return UserModel(
            ...                 id=1,
            ...                 uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            ...                 name="John",
            ...                 email="john@example.com"
            ...             )
            ...         return None
            ...
            >>> # Создание сервиса с моком репозитория
            >>> class MyService(BaseService):
            ...     ...
            ...
            >>> # Инициализация сервиса с сессией
            >>> db_session_instance = AsyncSession()
            >>> service = MyService(db_session_instance)
            >>> service._repository = MockRepository()
            >>>
            >>> async def main():
            ...     # Получение существующей сущности по UUID
            ...     test_uuid = UUID("123e4567-e89b-12d3-a456-426614174000")
            ...     result: UserModel = await service.get_by_uuid(test_uuid)
            ...     print(isinstance(result, UserModel))
            ...     # True
            ...     print(result.name)
            ...     # 'John'
            ...
            ...     # Получение несуществующей сущности (возвращается None)
            ...     result = await service.get_by_uuid(UUID("00000000-0000-0000-0000-000000000000"))
            ...     print(result is None)
            ...     # True
        """
        return await self._repository.get_by_uuid(uuid)
