"""Модуль базового репозитория."""

from datetime import UTC, datetime
from typing import Any, Generic, Type
from uuid import UUID, uuid4

from sqlalchemy import Delete, Result, Select, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from dh_bl_core.exceptions import NotFoundException

from ..logging import LogManager
from .exceptions import DeactivatedNotAllowed, EmptyDbSession, NoModelInRepository, NoPrimaryKeyInModel, NoUuidInModel
from .types import BaseModel


class BaseRepository(Generic[BaseModel]):
    """
    Базовый класс для репозиториев, предоставляющий стандартные операции с базой данных.

    Этот класс реализует основные CRUD-операции и служит родительским классом
    для всех конкретных репозиториев в приложении. Каждый наследующий репозиторий
    должен указать свою модель через атрибут _MODEL.

    Attributes:
        _MODEL (Type[BaseModelType]): Класс модели SQLAlchemy, с которой работает репозиторий.
        _LIMIT (int): Максимальное количество записей, возвращаемых методом list по умолчанию.
        _db_session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД.

    Examples:
        >>> from dh_bl_core.database import BaseModel, db_manager
        >>>
        >>> class User(BaseModel):
        ...     pass
        >>>
        >>> # Пример 1: Определение конкретного репозитория
        >>> class UserRepository(BaseRepository):
        ...     _MODEL = User
        ...
        >>> async def main():
        ...     db_session = await db_manager.get_db_session()
        ...     repo = UserRepository(db_session)
        ...     user = await repo.create({"name": "John", "email": "john@example.com"})
        ...     retrieved_user = await repo.get(user.id)

        >>> # Пример 2: Использование в сервисном слое
        >>> class UserService:
        ...     def __init__(self, db_session: AsyncSession):
        ...         self._repo = UserRepository(db_session)
        ...
        ...     async def get_user_by_id(self, user_id: int) -> User:
        ...         return await self._repo.get(user_id)
    """

    _MODEL: Type[BaseModel]
    _LIMIT: int = 100
    _LOGGER = LogManager("repos").logger

    def __init__(self, db_session: AsyncSession) -> None:
        """
        Инициализирует репозиторий с указанной сессией базы данных.

        Проверяет, что сессия не пуста и что репозиторий имеет определенную модель.
        Если проверки не проходят, выбрасываются соответствующие исключения.

        Args:
            db_session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД.

        Raises:
            EmptyDbSession: Если сессия подключения к БД не передана.
            NoModelInRepository: Если в репозиторий не передана модель данных.

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager
            >>>
            >>> class User(BaseModel):
            ...     pass
            >>> class UserRepository(BaseRepository):
            ...     _MODEL = User
            >>>
            >>> # Пример 1: Создание репозитория с валидной сессией
            >>> repo = UserRepository(db_session)
        """

        if not db_session:
            raise EmptyDbSession(self.__class__.__name__)

        if not self._MODEL:
            raise NoModelInRepository(self.__class__.__name__)

        self._db_session: AsyncSession = db_session
        self._LOGGER.debug(f"Репозиторий {self.__class__.__name__} инициализирован")

    async def create(self, payload: dict) -> BaseModel:
        """
        Создает новую запись в базе данных.

        Метод создает новую сущность на основе переданных данных, применяет
        предварительные настройки (генерация UUID, установка временных меток)
        и сохраняет в базу данных.

        Args:
            payload (dict): Словарь с данными для создания новой записи.

        Returns:
            BaseModelType: Созданная и сохраненная в БД модель.

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager
            >>>
            >>> class User(BaseModel):
            ...     pass
            >>> class UserRepository(BaseRepository):
            ...     _MODEL = User
            >>> class Product(BaseModel):
            ...     pass
            >>> class ProductRepository(BaseRepository):
            ...     _MODEL = Product
            >>>
            >>> async def main():
            ...     db_session = await db_manager.get_db_session()
            ...     # Пример 1: Создание репозитория с валидной сессией
            ...     user_repo = UserRepository(db_session)
            ...     # Пример 1: Создание нового пользователя
            ...     user_data = {
            ...         "name": "John Doe",
            ...         "email": "john@example.com",
            ...         "age": 30
            ...     }
            ...     user = await user_repo.create(user_data)
            ...     print(f"Создан пользователь с ID: {user.id}")
            ...
            ...     # Пример 2: Создание записи с автоматической генерацией полей
            ...     # (если модель имеет поля uuid, created_at)
            ...     product_repo = ProductRepository(db_session)
            ...     product = await product_repo.create({"name": "Laptop"})
            ...     print(f"UUID продукта: {product.uuid}")
            ...     print(f"Дата создания: {product.created_at}")
        """
        self._LOGGER.debug(f"Создание новой записи в репозитории {self.__class__.__name__}")
        self._before_create(payload)
        entity: BaseModel = self._get_filled_model(payload)

        self._db_session.add(entity)
        await self._db_session.commit()
        await self._db_session.refresh(entity)
        self._LOGGER.info(f"Создана новая запись в репозитории {self.__class__.__name__} - {entity.id}")

        return entity

    async def get(self, entity_id: int) -> BaseModel:
        """
        Получает запись из базы данных по её идентификатору.

        Метод выполняет асинхронный запрос к базе данных для получения записи
        по заданному id. Если запись не найдена, возвращает None.

        Args:
            entity_id (int): Идентификатор записи, которую необходимо получить.

        Returns:
            BaseModelType: Найденная модель или None, если запись не найдена.

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager
            >>>
            >>> class User(BaseModel):
            ...     pass
            >>>
            >>> class UserRepository(BaseRepository):
            ...     _MODEL = User
            ...
            >>> async def main():
            ...     db_session = await db_manager.get_db_session()
            ...     # Пример 1: Получение пользователя по id
            ...     user_repo = UserRepository(db_session)
            ...     user = await user_repo.get(123)
            ...     if user:
            ...         print(f"Найден пользователь: {user.name}")
            ...     else:
            ...         print("Пользователь не найден")

            >>> # Пример 2: Проверка существования записи
            >>> async def check_user_exists(user_id: int) -> bool:
            ...     db_session = await db_manager.get_db_session()
            ...     user_repo = UserRepository(db_session)
            ...     try:
            ...         return await user_repo.get(user_id)
            ...     except NotFoundException:
            ...         return False
        """
        self._LOGGER.info(f"Получение записи с id {entity_id} из репозитория {self.__class__.__name__}")
        return await self._get_by_field_name_and_value(self._MODEL.id, entity_id)

    async def get_by_uuid(self, uuid: UUID) -> BaseModel:
        """
        Получает запись из базы данных по её уникальному идентификатору (UUID).

        Метод выполняет асинхронный запрос к базе данных для получения записи
        по заданному UUID. Если запись не найдена, выбрасывается исключение.
        Требует, чтобы модель репозитория имела поле uuid.

        Args:
            uuid (UUID): Уникальный идентификатор записи, которую необходимо получить.

        Returns:
            BaseModelType: Найденная модель.

        Raises:
            NoUuidInModel: Если модель репозитория не имеет поля uuid.
            NotFoundException: Если запись с указанным UUID не найдена.

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager
            >>>
            >>> class User(BaseModel):
            ...     pass
            >>>
            >>> class UserRepository(BaseRepository):
            ...     _MODEL = User
            ...
            >>> async def main():
            ...     db_session = await db_manager.get_db_session()
            ...     user_repo = UserRepository(db_session)
            ...     # Пример 1: Получение пользователя по UUID
            ...     user = await user_repo.get_by_uuid(UUID("a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"))
            ...     print(f"Найден пользователь: {user.name}")
            ...
            ...     # Пример 2: Попытка получить несуществующую запись
            ...     from uuid import UUID
            ...     non_existent_uuid = UUID("00000000-0000-0000-0000-000000000000")
            ...     try:
            ...         user = await user_repo.get_by_uuid(non_existent_uuid)
            ...     except NotFoundException:
            ...         print("Пользователь с таким UUID не найден")
        """
        self._LOGGER.info(f"Получение записи с uuid {uuid} из репозитория {self.__class__.__name__}")
        if not hasattr(self._MODEL, "uuid"):
            raise NoUuidInModel(self._MODEL.__name__)

        return await self._get_by_field_name_and_value(getattr(self._MODEL, "uuid"), uuid)

    async def update(self, payload: dict) -> BaseModel:
        """
        Обновляет существующую запись в базе данных.

        Метод находит запись по id или uuid и обновляет её поля на основе переданных данных.
        Автоматически обновляет поле updated_at, если оно присутствует в модели.

        Args:
            payload (dict): Словарь с данными для обновления записи. Должен содержать
                          либо "id", либо "uuid" для идентификации записи.

        Returns:
            BaseModelType: Обновленная и сохраненная в БД модель.

        Raises:
            NoPrimaryKeyInModel: Если в payload не переданы ни id, ни uuid.
            NotFoundException: Если запись с указанным id или uuid не найдена.

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager
            >>>
            >>> class User(BaseModel):
            ...     pass
            >>>
            >>> class UserRepository(BaseRepository):
            ...     _MODEL = User
            ...
            >>> async def main():
            ...     db_session = await db_manager.get_db_session()
            ...     user_repo = UserRepository(db_session)
            ...     # Пример 1: Обновление пользователя по id
            ...     update_data = {
            ...         "id": 123,
            ...         "name": "Jane Doe",
            ...         "email": "jane@example.com"
            ...     }
            ...     updated_user = await user_repo.update(update_data)
            ...     print(f"Обновлено: {updated_user.name}, {updated_user.updated_at}")
            ...
            ...     # Пример 2: Обновление по uuid
            ...     update_data = {
            ...         "uuid": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
            ...         "status": "active"
            ...     }
            ...     updated_entity = await user_repo.update(update_data)
        """
        self._LOGGER.info(f"Обновление записи в репозитории {self.__class__.__name__}")
        if not payload.get("id") and not payload.get("uuid"):
            raise NoPrimaryKeyInModel(self._MODEL.__name__)

        if payload.get("id"):
            entity: BaseModel = await self.get(payload["id"])
        else:
            entity: BaseModel = await self.get_by_uuid(payload["uuid"])

        if "updated_at" in payload:
            payload["updated_at"] = datetime.now(UTC)

        entity = self._get_filled_model(payload, entity)

        self._db_session.add(entity)
        await self._db_session.commit()
        await self._db_session.refresh(entity)

        self._LOGGER.info(f"Обновлена запись в репозитории {self.__class__.__name__} - {entity.id}")

        return entity

    async def delete(self, entity_id: int) -> bool:
        """
        Удаляет запись из базы данных по её идентификатору.

        Метод реализует мягкое удаление (soft delete) для моделей, имеющих поле deleted_at,
        устанавливая временную метку удаления. Для моделей без этого поля выполняется
        физическое удаление записи.

        Args:
            entity_id (int): Идентификатор записи, которую необходимо удалить.

        Returns:
            bool: True, если удаление прошло успешно, False в случае ошибки.

        Raises:
            NotFoundException: Если запись с указанным id не найдена.

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager, SoftDeleteMixin
            >>>
            >>> class User(BaseModel, SoftDeleteMixin):
            ...     pass
            ...
            >>> class Log(BaseModel):
            ...     pass
            >>>
            >>> class UserRepository(BaseRepository):
            ...     _MODEL = User
            ...
            >>> class LogRepository(BaseRepository):
            ...     _MODEL = Log
            ...
            >>> async def main():
            ...     db_session = await db_manager.get_db_session()
            ...     user_repo = UserRepository(db_session)
            ...     log_repo = LogRepository(db_session)
            ...     # Пример 1: Мягкое удаление пользователя (с полем deleted_at)
            ...     result = await user_repo.delete(123)
            ...     if result:
            ...         print("Пользователь успешно помечен как удаленный")
            ...
            ...     # Пример 2: Физическое удаление записи (без поля deleted_at)
            ...     result = await log_repo.delete(456)
            ...     if result:
            ...         print("Запись журнала физически удалена из БД")
        """
        self._LOGGER.info(f"Удаление записи с id {entity_id} из репозитория {self.__class__.__name__}")
        entity: BaseModel = await self.get(entity_id)

        if hasattr(entity, "deleted_at") and not entity.deleted_at:
            self._LOGGER.debug(f"Использование мягкого удаления для модели {self._MODEL.__name__}")
            entity.deleted_at = datetime.now(UTC)
            self._db_session.add(entity)
            await self._db_session.commit()
            self._LOGGER.info(f"Мягкое удаление записи с id {entity_id} из репозитория {self.__class__.__name__}")
            return True

        stmt: Delete = delete(self._MODEL).where(self._MODEL.id == entity_id)
        await self._db_session.execute(stmt)
        await self._db_session.commit()
        self._LOGGER.info(f"Физическое удаление записи с id {entity_id} из репозитория {self.__class__.__name__}")

        return True

    async def delete_by_uuid(self, uuid: UUID) -> bool:
        """
        Удаляет запись из базы данных по её уникальному идентификатору (UUID).

        Метод находит запись по UUID и удаляет её, используя стандартный метод delete.
        Поддерживает как мягкое, так и физическое удаление в зависимости от модели.

        Args:
            uuid (UUID): Уникальный идентификатор записи, которую необходимо удалить.

        Returns:
            bool: True, если удаление прошло успешно, False в случае ошибки.

        Raises:
            NoUuidInModel: Если модель репозитория не имеет поля uuid.
            NotFoundException: Если запись с указанным UUID не найдена.

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager
            >>>
            >>> class User(BaseModel):
            ...     pass
            >>>
            >>> class UserRepository(BaseRepository):
            ...     _MODEL = User
            ...
            >>> async def main():
            ...     db_session = await db_manager.get_db_session()
            ...     user_repo = UserRepository(db_session)
            ...     # Пример: Удаление пользователя по UUID
            ...     user_uuid = UUID("a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8")
            ...     result = await user_repo.delete_by_uuid(user_uuid)
            ...     if result:
            ...         print("Пользователь успешно удален")
        """
        self._LOGGER.info(f"Удаление записи с uuid {uuid} из репозитория {self.__class__.__name__}")
        entity: BaseModel = await self.get_by_uuid(uuid)
        return await self.delete(entity.id)

    async def toggle_deactivate(self, entity_id: int) -> bool:
        """
        Переключает статус деактивации записи в базе данных.

        Метод изменяет состояние поля deactivated_at: если оно пустое, устанавливает
        текущую временную метку; если уже содержит значение, очищает его (реактивация).
        Требует, чтобы модель имела поле deactivated_at.

        Args:
            entity_id (int): Идентификатор записи, статус которой необходимо переключить.

        Returns:
            bool: True, если операция прошла успешно, False в случае ошибки.

        Raises:
            DeactivatedNotAllowed: Если модель репозитория не поддерживает деактивацию
                                (не имеет поля deactivated_at).
            NotFoundException: Если запись с указанным id не найдена.

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager
            >>>
            >>> class User(BaseModel):
            ...     pass
            >>>
            >>> class UserRepository(BaseRepository):
            ...     _MODEL = User
            ...
            >>> async def main():
            ...     db_session = await db_manager.get_db_session()
            ...     user_repo = UserRepository(db_session)
            ...     # Пример 1: Деактивация пользователя
            ...     result = await user_repo.toggle_deactivate(123)
            ...     if result:
            ...         user = await user_repo.get(123)
            ...         print(f"Статус деактивации: {user.deactivated_at is not None}")
            ...
            ...     # Пример 2: Реактивация ранее деактивированного пользователя
            ...     # (повторный вызов для того же пользователя)
            ...     result = await user_repo.toggle_deactivate(123)
            ...     user = await user_repo.get(123)
            ...     print(f"Пользователь снова активен: {user.deactivated_at is None}")
        """
        self._LOGGER.info(
            f"Переключение деактивации для записи с id {entity_id} в репозитории {self.__class__.__name__}"
        )
        if not hasattr(self._MODEL, "deactivated_at"):
            raise DeactivatedNotAllowed(self._MODEL.__name__)

        entity: BaseModel = await self.get(entity_id)

        if entity.deactivated_at:
            self._LOGGER.debug("Очистка поля deactivated_at")
            entity.deactivated_at = None
        else:
            self._LOGGER.debug("Установка поля deactivated_at")
            entity.deactivated_at = datetime.now(UTC)

        self._db_session.add(entity)
        await self._db_session.commit()
        self._LOGGER.info(
            f"Переключение деактивации для записи с id {entity_id} в репозитории {self.__class__.__name__}"
        )
        return True

    async def list(
        self, filters: dict | None = None, navigation: dict | None = None, sorting: dict | None = None
    ) -> list[BaseModel]:
        """
        Получает список записей из базы данных с возможностью фильтрации, пагинации и сортировки.

        Метод возвращает список записей с применением указанных фильтров, параметров
        навигации (пагинации) и сортировки. По умолчанию используется лимит, определенный
        в атрибуте _LIMIT.

        Args:
            filters (dict | None): Словарь с параметрами фильтрации. Поддерживаемые фильтры:
                - "ids": список ID для фильтрации
                - "uuids": список UUID для фильтрации
                - "only_deleted": только удаленные записи
                - "with_deleted": включая удаленные записи
                - "only_deactivated": только деактивированные записи
                - "with_deactivated": включая деактивированные записи
            navigation (dict | None): Словарь с параметрами пагинации:
                - "limit": количество записей на странице (по умолчанию _LIMIT)
                - "offset": смещение для пагинации
            sorting (dict | None): Словарь с параметрами сортировки:
                - "field": имя поля для сортировки
                - "direction": направление сортировки (asc/desc)

        Returns:
            list[BaseModelType]: Список моделей, соответствующих критериям.

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager
            >>>
            >>> class User(BaseModel):
            ...     pass
            >>>
            >>> class UserRepository(BaseRepository):
            ...     _MODEL = User
            ...
            >>> async def main():
            ...     db_session = await db_manager.get_db_session()
            ...     user_repo = UserRepository(db_session)
            ...     # Пример 1: Получение всех пользователей с пагинацией
            ...     users = await user_repo.list(navigation={"limit": 10, "offset": 0})
            ...     print(f"Получено {len(users)} пользователей")
            ...
            ...     # Пример 2: Фильтрация по списку ID и сортировка
            ...     users = await user_repo.list(
            ...         filters={"ids": [1, 2, 3]},
            ...         sorting={"field": "name", "direction": "asc"}
            ...     )
            ...     for user in users:
            ...         print(user.name)
            ...
            ...     # Пример 3: Получение только удаленных записей
            ...     deleted_users = await user_repo.list(filters={"only_deleted": True})
            ...     print(f"Найдено {len(deleted_users)} удаленных пользователей")
        """
        self._LOGGER.info(f"Получение списка записей из репозитория {self.__class__.__name__}")
        stmt: Select = select(self._MODEL)

        if filters:
            stmt = self._apply_filters(stmt, filters)

        if sorting:
            if sorting.get("field") and sorting.get("direction"):
                stmt = stmt.order_by(getattr(self._MODEL, sorting["field"]), sorting["direction"])

        if not navigation:
            navigation = {"limit": self._LIMIT, "offset": 0}

        stmt = stmt.limit(navigation.get("limit")).offset(navigation.get("offset"))

        result: Result[BaseModel] = await self._db_session.execute(stmt)

        self._LOGGER.info(f"Получены записи из репозитория {self.__class__.__name__}")

        return list(result.scalars().all())

    def _before_create(self, payload: dict) -> None:
        """
        Подготавливает данные перед созданием новой записи.

        Метод автоматически добавляет системные поля, если они существуют в модели,
        но отсутствуют в переданных данных: генерирует UUID, устанавливает временные
        метки created_at и updated_at.

        Args:
            payload (dict): Словарь с данными для создания записи, который будет модифицирован.

        Note:
            Этот метод вызывается автоматически при создании новой записи через метод create.
            Не предназначен для прямого вызова извне.

        Examples:
            >>> # Пример: Автоматическая генерация полей при создании
            >>> # (внутреннее использование при вызове create)
            >>> new_payload = {"name": "Test"}
            >>> self._before_create(new_payload)
        """
        if hasattr(self._MODEL, "uuid") and not payload.get("uuid"):
            self._LOGGER.debug(f"Генерация UUID для модели {self._MODEL.__name__}")
            payload["uuid"] = uuid4()

        if hasattr(self._MODEL, "created_at") and not payload.get("created_at"):
            self._LOGGER.debug(f"Установка created_at для модели {self._MODEL.__name__}")
            payload["created_at"] = datetime.now(UTC)

        if hasattr(self._MODEL, "updated_at") and not payload.get("updated_at"):
            self._LOGGER.debug(f"Установка updated_at для модели {self._MODEL.__name__}")
            payload["updated_at"] = datetime.now(UTC)

    def _get_filled_model(self, payload: dict, model: BaseModel | None = None) -> BaseModel:
        """
        Заполняет модель данными из словаря.

        Метод создает новую или использует существующую модель и заполняет её поля
        значениями из переданного словаря. Поля, которых нет в модели, игнорируются.

        Args:
            payload (dict): Словарь с данными для заполнения модели.
            model (BaseModelType | None): Существующая модель для обновления или None для создания новой.

        Returns:
            BaseModelType: Заполненная модель.

        Note:
            Этот метод вызывается автоматически при создании и обновлении записей.
            Не предназначен для прямого вызова извне.

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager
            >>>
            >>> class User(BaseModel):
            ...     name: str
            ...     age: int
            >>>
            >>> # Пример 1: Создание новой модели
            >>> user_payload = {"name": "John", "age": 30}
            >>> user_model: User = self._get_filled_model(payload)
            >>> print(user_model.name)  # John
            >>> print(user_model.age)   # 30

            >>> # Пример 2: Обновление существующей модели
            >>> existing_model = User(id=1, name="Old Name")
            >>> user_payload = {"name": "New Name"}
            >>> updated_model: User = self._get_filled_model(user_payload, existing_model)
            >>> print(updated_model.name)  # New Name
        """
        if not model:
            model = self._MODEL()

        for key, value in payload.items():
            if not hasattr(model, key):
                self._LOGGER.debug(f"Поле {key} не найдено в модели {self._MODEL.__name__}")
                continue

            self._LOGGER.debug(f"Заполнение поля {key} модели {self._MODEL.__name__} значением {value}")
            setattr(model, key, value)

        return model

    async def _get_by_field_name_and_value(self, field: Mapped[int] | Mapped[UUID], value: Any) -> BaseModel:
        """
        Получает запись из базы данных по значению указанного поля.

        Метод выполняет асинхронный запрос к базе данных для получения записи
        по заданному полю и значению. Если запись не найдена, выбрасывается исключение.

        Args:
            field (Mapped[int] | Mapped[UUID]): Поле модели, по которому выполняется поиск.
            value (Any): Значение для поиска.

        Returns:
            BaseModelType: Найденная модель.

        Raises:
            NotFoundException: Если запись с указанным значением поля не найдена.

        Note:
            Этот метод является внутренним и используется методами get и get_by_uuid.
            Не предназначен для прямого вызова извне.

        Examples:
            >>> async def main():
            ...     # Пример: Внутреннее использование при получении по ID
            ...     # (вызывается автоматически методом get)
            ...     entity = await self._get_by_field_name_and_value(self._MODEL.id, 123)
            ...     print(entity) # Модель с id=123
        """
        stmt: Select = select(self._MODEL).where(field == value)
        result: Result[BaseModel] = await self._db_session.execute(stmt)
        entity: BaseModel | None = result.scalar_one_or_none()

        if not entity:
            raise NotFoundException()

        return entity

    def _apply_filters(self, stmt: Select, filters: dict) -> Select:
        """
        Применяет фильтры к SQL-запросу.

        Метод модифицирует переданный SQL-запрос, добавляя условия фильтрации
        на основе предоставленных параметров. Обрабатывает фильтрацию по ID,
        UUID, статусу удаления и деактивации.

        Args:
            stmt (Select): Объект SQL-запроса SQLAlchemy для модификации.
            filters (dict): Словарь с параметрами фильтрации.

        Returns:
            Select: Модифицированный SQL-запрос с примененными фильтрами.

        Note:
            Этот метод является внутренним и вызывается автоматически методом list.
            Не предназначен для прямого вызова извне.

        Filter Options:
            - "ids": фильтрация по списку ID
            - "uuids": фильтрация по списку UUID (только если модель имеет поле uuid)
            - "only_deleted": только удаленные записи (с заполненным deleted_at)
            - "with_deleted": включая удаленные записи (по умолчанию - только активные)
            - "only_deactivated": только деактивированные записи
            - "with_deactivated": включая деактивированные записи (по умолчанию - только активные)

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager
            >>>
            >>> class User(BaseModel):
            ...     pass
            >>> # Пример: Внутреннее использование при вызове list
            >>> # (вызывается автоматически)
            >>> select_stmt: Select = select(User)
            >>> user_filters = {"ids": [1, 2, 3], "only_deleted": True}
            >>> filtered_select_stmt = self._apply_filters(select_stmt, user_filters)
            >>> # Результирующий запрос будет содержать условия:
            >>> # WHERE id IN (1, 2, 3) AND deleted_at IS NOT NULL
        """
        self._apply_primary_ids_filters(stmt, filters)
        self._apply_deleted_deactivated_filters(stmt, filters)

        return stmt

    def _apply_primary_ids_filters(self, stmt: Select, filters: dict) -> Select:
        """
        Применяет фильтры по первичным идентификаторам (ID и UUID) к SQL-запросу.

        Метод добавляет условия фильтрации по списку ID и/или UUID, если они присутствуют
        в параметрах фильтрации.

        Args:
            stmt (Select): Объект SQL-запроса SQLAlchemy для модификации.
            filters (dict): Словарь с параметрами фильтрации, содержащий:
                - "ids": список ID для фильтрации
                - "uuids": список UUID для фильтрации

        Returns:
            Select: Модифицированный SQL-запрос с условиями фильтрации по ID и UUID.

        Note:
            Этот метод является внутренним и вызывается методом _apply_filters.
            Не предназначен для прямого вызова извне.

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager
            >>>
            >>> class User(BaseModel):
            ...     pass
            >>> # Пример: Внутреннее использование при вызове list
            >>> # (вызывается автоматически)
            >>> select_stmt: Select = select(User)
            >>> user_filters = {"ids": [1, 2, 3], "uuids": [UUID("..."), UUID("...")]}
            >>> filtered_select_stmt = self._apply_filters(select_stmt, user_filters)
            >>> # Результирующий запрос будет содержать условия:
            >>> # WHERE id IN (1, 2, 3) AND uuid IN (uuid1, uuid2)
        """
        self._LOGGER.debug(f"Применение фильтров к запросу: {filters}")
        if filters.get("ids"):
            self._LOGGER.debug(f"Фильтрация по списку ID: {filters['ids']}")
            stmt = stmt.where(self._MODEL.id.in_(filters["ids"]))

        if filters.get("uuids") and hasattr(self._MODEL, "uuid"):
            self._LOGGER.debug(f"Фильтрация по списку UUID: {filters['uuids']}")
            stmt = stmt.where(self._MODEL.uuid.in_(filters["uuids"]))

        return stmt

    def _apply_deleted_deactivated_filters(self, stmt: Select, filters: dict) -> Select:
        """
        Применяет фильтры по статусу удаления и деактивации к SQL-запросу.

        Метод добавляет условия фильтрации по полям deleted_at и deactivated_at,
        если они существуют в модели. Обрабатывает фильтрацию только удаленных,
        только деактивированных записей и включения удаленных/деактивированных записей.

        Args:
            stmt (Select): Объект SQL-запроса SQLAlchemy для модификации.
            filters (dict): Словарь с параметрами фильтрации, содержащий:
                - "only_deleted": фильтр только для удаленных записей
                - "with_deleted": включение удаленных записей в результат
                - "only_deactivated": фильтр только для деактивированных записей
                - "with_deactivated": включение деактивированных записей в результат

        Returns:
            Select: Модифицированный SQL-запрос с условиями фильтрации по статусу удаления и деактивации.

        Note:
            Этот метод является внутренним и вызывается методом _apply_filters.
            Не предназначен для прямого вызова извне.

        Examples:
            >>> from dh_bl_core.database import BaseModel, db_manager
            >>>
            >>> class User(BaseModel):
            ...     pass
            >>> # Пример 1: Фильтрация только удаленных записей
            >>> select_stmt = select(User)
            >>> user_filters = {"only_deleted": True}
            >>> filtered_select_stmt = self._apply_deleted_deactivated_filters(select_stmt, user_filters)
            >>> # Результирующий запрос будет содержать условие:
            >>> # WHERE deleted_at IS NOT NULL

            >>> # Пример 2: Фильтрация только активных записей (по умолчанию)
            >>> select_stmt = select(User)
            >>> user_filters = {}
            >>> filtered_select_stmt = self._apply_deleted_deactivated_filters(select_stmt, user_filters)
            >>> # Результирующий запрос будет содержать условие:
            >>> # WHERE deleted_at IS NULL
        """
        self._LOGGER.debug(f"Применение фильтров по статусу удаления и деактивации: {filters}")
        if hasattr(self._MODEL, "deleted_at"):
            self._LOGGER.debug("Модель содержит поле deleted_at")
            if not filters.get("only_deleted") and not filters.get("with_deleted"):
                self._LOGGER.debug("Фильтрация только активных записей")
                stmt = stmt.where(self._MODEL.deleted_at.is_(None))

            if filters.get("only_deleted"):
                self._LOGGER.debug("Фильтрация только удаленных записей")
                stmt = stmt.where(self._MODEL.deleted_at.isnot(None))

        if hasattr(self._MODEL, "deactivated_at"):
            self._LOGGER.debug("Модель содержит поле deactivated_at")
            if filters.get("only_deactivated"):
                self._LOGGER.debug("Фильтрация только деактивированных записей")
                stmt = stmt.where(self._MODEL.deactivated_at.isnot(None))
            elif not filters.get("with_deactivated") and not filters.get("only_deactivated"):
                self._LOGGER.debug("Фильтрация только активных записей")
                stmt = stmt.where(self._MODEL.deactivated_at.is_(None))

        return stmt
