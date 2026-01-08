"""Исключения при работе с БД."""

from dh_bl_core.exceptions import InternalServerErrorException

from .consts import MAX_PORT_NUMBER, MIN_PORT_NUMBER


class DbMangerNotInit(InternalServerErrorException):
    """
    Исключение, возникающее при попытке использования менеджера базы данных до его инициализации.

    Это исключение является подклассом InternalServerErrorException и выбрасывается,
    когда происходит обращение к функциональности работы с БД, но менеджер еще не был инициализирован.

    Attributes:
        _DETAILS (str): Описание ошибки, которое будет включено в ответ.

    Examples:
        >>> # Пример 1: Попытка использовать менеджер до инициализации
        >>> from dh_bl_core.database import db_manager, AsyncDatabaseConnectionManager
        >>> from logging import getLogger
        >>> logger = getLogger(__name__)
        >>>
        >>> try:
        ...     db = db_manager.get_instance()
        ...     db.execute_query("SELECT * FROM users")
        ... except DbMangerNotInit as e:
        ...     print(f"Ошибка: {e}")
        ...
        Ошибка: Менеджер для работы с БД не инициализирован

        >>> # Пример 2: Обработка исключения при старте приложения
        >>> def init_database():
        ...     try:
        ...         AsyncDatabaseConnectionManager.init({})
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
        >>> from dh_bl_core.database import BaseModel
        >>>
        >>> class User(BaseModel):
        ...     pass
        >>>
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
        >>> from dh_bl_core.database import BaseModel, db_manager
        >>> # Пример 2: Проверка модели в базовом классе репозитория
        >>> class BaseRepository:
        ...     def __init__(self, session, model):
        ...         self.session = session
        ...         self.model = model
        ...         if model is None:
        ...             raise NoModelInRepository(self.__class__.__name__)
        ...
        >>> async def main():
        ...     db_session = await db_manager.get_db_session()
        ...     repo = BaseRepository(db_session, None)  # raises NoModelInRepository
    """

    def __init__(self, name: str) -> None:
        super().__init__(details=f'В репозиторий "{name}" не передана модель данных')


class NoPrimaryKeyInModel(InternalServerErrorException):
    """
    Исключение, возникающее при попытке обновить или удалить запись без указания первичного ключа.

    Это исключение является подклассом InternalServerErrorException и выбрасывается,
    когда в метод update передается payload без идентификатора (id или uuid),
    необходимого для поиска записи в базе данных.

    Examples:
        >>> from logging import getLogger
        >>> from dh_bl_core.database import BaseRepository, BaseModel, db_manager
        >>> logger = getLogger(__name__)
        >>> # Пример 1: Попытка обновить запись без указания id или uuid
        >>> async def main():
        >>>     db_session = await db_manager.get_db_session()
        >>>     user_repo = BaseRepository(db_session)
        ...     update_data = {"name": "Updated Name"}  # отсутствуют id и uuid
        ...     try:
        ...         updated_user = await user_repo.update(update_data)
        ...     except NoPrimaryKeyInModel as e:
        ...         print(f"Ошибка: {e}")
        ...
        Ошибка: В модели "User" не найден первичный ключ

        >>> # Пример 2: Проверка наличия первичного ключа перед обновлением
        >>> async def safe_update(repo: BaseRepository, payload: dict):
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

    Examples:
        >>> from sqlalchemy import Column, Integer, String
        >>> from uuid import UUID
        >>> from dh_bl_core.database import BaseRepository, BaseModel, db_manager
        >>>
        >>> # Пример 1: Попытка получить запись по UUID для модели без поля uuid
        >>> class SimpleModel(BaseModel):
        ...     id = Column(Integer, primary_key=True)
        ...     name = Column(String)
        ...
        >>> class SimpleRepository(BaseRepository):
        ...     _MODEL = SimpleModel
        ...
        >>> async def main():
        ...     db_session = await db_manager.get_db_session()
        ...     repo = SimpleRepository(db_session)
        ...     try:
        ...         entity = await repo.get_by_uuid(UUID("...")
        ...     except NoUuidInModel as e:
        ...         print(f"Ошибка: {e}")
        ...
        Ошибка: В модели "SimpleModel" нет столбца "uuid"
    """

    def __init__(self, name: str) -> None:
        super().__init__(details=f'В модели "{name}" нет столбца "uuid"')


class DeactivatedNotAllowed(InternalServerErrorException):
    """
    Исключение, возникающее при попытке деактивировать запись модели, не поддерживающей деактивацию.

    Это исключение является подклассом InternalServerErrorException и выбрасывается,
    когда вызывается метод toggle_deactivate для репозитория, модель которого
    не имеет поля deactivated_at.

    Examples:
        >>> from sqlalchemy import Column, Integer, String
        >>> from dh_bl_core.database import BaseRepository, BaseModel, db_manager
        >>>
        >>> # Пример 1: Попытка деактивировать запись для модели без поля deactivated_at
        >>> class ActiveOnlyModel(BaseModel):
        ...     __tablename__ = "active_only_models"
        ...     id = Column(Integer, primary_key=True)
        ...     name = Column(String)
        ...     # Нет поля deactivated_at
        ...
        >>> class ActiveOnlyRepository(BaseRepository):
        ...     _MODEL = ActiveOnlyModel
        ...
        >>> async def main():
        ...     db_session = await db_manager.get_db_session()
        ...     repo = ActiveOnlyRepository(db_session)
        ...     try:
        ...         await repo.toggle_deactivate(123)
        ...     except DeactivatedNotAllowed as e:
        ...         print(f"Ошибка: {e}")
        ...
        Ошибка: Деактивация для модели "ActiveOnlyModel" недоступна
    """

    def __init__(self, name: str) -> None:
        super().__init__(details=f'Деактивация для модели "{name}" недоступна')


class InvalidDbHostException(InternalServerErrorException):
    """
    Исключение для некорректного хоста подключения к базе данных.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда хост базы данных не проходит валидацию (пустой или некорректный).

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise InvalidDbHostException()
        Traceback (most recent call last):
        ...
        InvalidDbHostException: Некорректный хост для подключения к БД
    """

    _DETAILS = "Некорректный хост для подключения к БД"


class InvalidDbUsernameException(InternalServerErrorException):
    """
    Исключение для некорректного имени пользователя базы данных.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда имя пользователя базы данных не проходит валидацию
    (пустое или некорректное).

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise InvalidDbUsernameException()
        Traceback (most recent call last):
        ...
        InvalidDbUsernameException: Некорректное имя пользователя для подключения к БД
    """

    _DETAILS = "Некорректное имя пользователя для подключения к БД"


class InvalidDbPasswordException(InternalServerErrorException):
    """
    Исключение для некорректного пароля базы данных.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда пароль базы данных не проходит валидацию (пустой).

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise InvalidDbPasswordException()
        Traceback (most recent call last):
        ...
        InvalidDbPasswordException: Некорректный пароль для подключения к БД
    """

    _DETAILS = "Некорректный пароль для подключения к БД"


class InvalidDbNameException(InternalServerErrorException):
    """
    Исключение для некорректного названия базы данных.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда название базы данных не проходит валидацию (пустое или некорректное).

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise InvalidDbNameException()
        Traceback (most recent call last):
        ...
        InvalidDbNameException: Некорректное имя БД
    """

    _DETAILS = "Некорректное имя БД"


class InvalidDbPortException(InternalServerErrorException):
    """
    Исключение для некорректного порта подключения к базе данных.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда порт базы данных выходит за допустимый диапазон.
    Допустимый диапазон: от MIN_PORT_NUMBER до MAX_PORT_NUMBER.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию, содержащее
            допустимый диапазон портов.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise InvalidDbPortException()
        Traceback (most recent call last):
        ...
        InvalidDbPortException: Некорректный порт для подключения к БД. Допустимый диапазон: от 1 до 65535
    """

    _DETAILS = (
        f"Некорректный порт для подключения к БД. " f"Допустимый диапазон: от {MIN_PORT_NUMBER} до {MAX_PORT_NUMBER}"
    )
