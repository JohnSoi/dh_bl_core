"""Исключения при работе с БД."""

from dh_bl_core.exceptions import InternalServerErrorException


class DbMangerNotInit(InternalServerErrorException):
    """
    Исключение, возникающее при попытке использования менеджера базы данных до его инициализации.

    Это исключение является подклассом InternalServerErrorException и выбрасывается,
    когда происходит обращение к функциональности работы с БД, но менеджер еще не был инициализирован.

    Attributes:
        _DETAILS (str): Описание ошибки, которое будет включено в ответ.

    Examples:
        >>> # Пример 1: Попытка использовать менеджер до инициализации
        >>> from dh_bl_core.database import DatabaseManager
        >>> try:
        ...     db = DatabaseManager.get_instance()
        ...     db.execute_query("SELECT * FROM users")
        ... except DbMangerNotInit as e:
        ...     print(f"Ошибка: {e}")
        ...
        Ошибка: Менеджер для работы с БД не инициализирован

        >>> # Пример 2: Обработка исключения при старте приложения
        >>> def init_database():
        ...     try:
        ...         DatabaseManager.initialize(connection_params)
        ...     except DbMangerNotInit:
        ...         logger.error("Не удалось инициализировать менеджер БД")
        ...         raise

    """

    _DETAILS = "Менеджер для работы с БД не инициализирован"


class EmptyDbSession(InternalServerErrorException):
    """
    Исключение, возникающее при попытке использования репозитория без переданной сессии подключения к базе данных.

    Это исключение является подклассом InternalServerErrorException и выбрасывается,
    когда в репозиторий не была передана сессия подключения к БД, что делает невозможным выполнение операций с данными.

    Examples:
        >>> # Пример 1: Попытка создать репозиторий без сессии
        >>> class UserRepository:
        ...     def __init__(self, session):
        ...         if session is None:
        ...             raise EmptyDbSession(self.__class__.__name__)
        ...
        >>> try:
        ...     repo = UserRepository(None)
        ... except EmptyDbSession as e:
        ...     print(f"Ошибка: {e}")
        ...
        Ошибка: В репозиторий "UserRepository" не передана сессия подключения к БД

        >>> # Пример 2: Проверка сессии в базовом классе репозитория
        >>> class BaseRepository:
        ...     def __init__(self, session, model):
        ...         self.session = session
        ...         self.model = model
        ...         if session is None:
        ...             raise EmptyDbSession(self.__class__.__name__)
        ...
        >>> repo = BaseRepository(None, User)  # raises EmptyDbSession
    """

    def __init__(self, name: str) -> None:
        super().__init__(details=f'В репозиторий "{name}" не передана сессия подключения к БД')


class NoModelInRepository(InternalServerErrorException):
    """
    Исключение, возникающее при попытке использования репозитория без переданной модели данных.

    Это исключение является подклассом InternalServerErrorException и выбрасывается,
    когда в репозиторий не была передана модель данных, что делает невозможным выполнение операций с данными.

    Examples:
        >>> # Пример 1: Попытка создать репозиторий без модели
        >>> class UserRepository:
        ...     def __init__(self, model):
        ...         if model is None:
        ...             raise NoModelInRepository(self.__class__.__name__)
        ...
        >>> try:
        ...     repo = UserRepository(None)
        ... except NoModelInRepository as e:
        ...     print(f"Ошибка: {e}")
        ...
        Ошибка: В репозиторий "UserRepository" не передана модель данных

        >>> # Пример 2: Проверка модели в базовом классе репозитория
        >>> class BaseRepository:
        ...     def __init__(self, session, model):
        ...         self.session = session
        ...         self.model = model
        ...         if model is None:
        ...             raise NoModelInRepository(self.__class__.__name__)
        ...
        >>> repo = BaseRepository(db_session, None)  # raises NoModelInRepository
    """

    def __init__(self, name: str) -> None:
        super().__init__(details=f'В репозиторий "{name}" не передана модель данных')


class NoPrimaryKeyInModel(InternalServerErrorException):
    """
    Исключение, возникающее при попытке обновить или удалить запись без указания первичного ключа.

    Это исключение является подклассом InternalServerErrorException и выбрасывается,
    когда в метод update передается payload без идентификатора (id или uuid),
    необходимого для поиска записи в базе данных.

    Attributes:
        name (str): Имя модели, для которой не указан первичный ключ.

    Examples:
        >>> # Пример 1: Попытка обновить запись без указания id или uuid
        >>> update_data = {"name": "Updated Name"}  # отсутствуют id и uuid
        >>> try:
        ...     updated_user = await user_repo.update(update_data)
        ... except NoPrimaryKeyInModel as e:
        ...     print(f"Ошибка: {e}")
        ...
        Ошибка: В модели "User" не найден первичный ключ

        >>> # Пример 2: Проверка наличия первичного ключа перед обновлением
        >>> async def safe_update(repo: BaseRepository, payload: dict) -> BaseModelType | None:
        ...     if not payload.get("id") and not payload.get("uuid"):
        ...         logger.warning("Попытка обновления без указания идентификатора")
        ...         return None
        ...     return await repo.update(payload)
    """

    def __init__(self, name: str) -> None:
        super().__init__(details=f'В модели "{name}" не найден первичный ключ')


class NoUuidInModel(InternalServerErrorException):
    """
    Исключение, возникающее при попытке использовать UUID-функциональность для модели, не имеющей поля uuid.

    Это исключение является подклассом InternalServerErrorException и выбрасывается,
    когда вызывается метод, использующий UUID (например, get_by_uuid или delete_by_uuid),
    но модель репозитория не имеет поля uuid.

    Attributes:
        name (str): Имя модели, не имеющей поля uuid.

    Examples:
        >>> # Пример 1: Попытка получить запись по UUID для модели без поля uuid
        >>> class SimpleModel(Base):
        ...     __tablename__ = "simple_models"
        ...     id = Column(Integer, primary_key=True)
        ...     name = Column(String)
        ...
        >>> class SimpleRepository(BaseRepository):
        ...     _MODEL = SimpleModel
        ...
        >>> repo = SimpleRepository(db_session)
        >>> try:
        ...     entity = await repo.get_by_uuid(some_uuid)
        ... except NoUuidInModel as e:
        ...     print(f"Ошибка: {e}")
        ...
        Ошибка: В модели "SimpleModel" нет столбца "uuid"

        >>> # Пример 2: Проверка наличия поля uuid перед использованием
        >>> def can_use_uuid_operations(repo: BaseRepository) -> bool:
        ...     return hasattr(repo._MODEL, "uuid")
        ...
        >>> if can_use_uuid_operations(repo):
        ...     entity = await repo.get_by_uuid(entity_uuid)
        ... else:
        ...     print("Модель не поддерживает операции с UUID")
    """

    def __init__(self, name: str) -> None:
        super().__init__(details=f'В модели "{name}" нет столбца "uuid"')


class DeactivatedNotAllowed(InternalServerErrorException):
    """
    Исключение, возникающее при попытке деактивировать запись модели, не поддерживающей деактивацию.

    Это исключение является подклассом InternalServerErrorException и выбрасывается,
    когда вызывается метод toggle_deactivate для репозитория, модель которого
    не имеет поля deactivated_at.

    Attributes:
        name (str): Имя модели, не поддерживающей деактивацию.

    Examples:
        >>> # Пример 1: Попытка деактивировать запись для модели без поля deactivated_at
        >>> class ActiveOnlyModel(Base):
        ...     __tablename__ = "active_only_models"
        ...     id = Column(Integer, primary_key=True)
        ...     name = Column(String)
        ...     # Нет поля deactivated_at
        ...
        >>> class ActiveOnlyRepository(BaseRepository):
        ...     _MODEL = ActiveOnlyModel
        ...
        >>> repo = ActiveOnlyRepository(db_session)
        >>> try:
        ...     await repo.toggle_deactivate(123)
        ... except DeactivatedNotAllowed as e:
        ...     print(f"Ошибка: {e}")
        ...
        Ошибка: Деактивация для модели "ActiveOnlyModel" недоступна

        >>> # Пример 2: Проверка поддержки деактивации перед вызовом
        >>> def supports_deactivation(repo: BaseRepository) -> bool:
        ...     return hasattr(repo._MODEL, "deactivated_at")
        ...
        >>> if supports_deactivation(repo):
        ...     await repo.toggle_deactivate(entity_id)
        ... else:
        ...     print("Модель не поддерживает деактивацию")
    """

    def __init__(self, name: str) -> None:
        super().__init__(details=f'Деактивация для модели "{name}" недоступна')
