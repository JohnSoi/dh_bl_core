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
