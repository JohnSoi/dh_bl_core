"""Менеджер логирования."""
from sys import stdout

from loguru import logger

from .config import LoggingConfig


class LogManager:
    """
    Менеджер логирования, настраивающий и управляющий логгерами приложения.

    Этот класс предоставляет централизованный способ настройки логирования
    с поддержкой вывода в консоль и файл с различными уровнями и форматами.

    Attributes:
        _settings (LoggingConfig): Конфигурация логирования, содержащая
            настройки для консольного и файлового вывода.
        _prefix (str): Префикс, добавляемый к каждому сообщению лога для
            идентификации источника.
        _logger (Logger): Экземпляр логгера Loguru, настроенный с указанным префиксом.

    Examples:
        >>> # Пример 1: Создание менеджера логирования с настройками по умолчанию
        >>> logger_manager = LogManager("my_app")
        >>> custom_logger = logger_manager.logger
        >>> custom_logger.info("Приложение запущено")
        >>> # [my_app] Приложение запущено
        >>>
        >>> # Пример 2: Создание менеджера с кастомной конфигурацией
        >>> from dh_bl_core.logging.config import LoggingConfig
        >>> from dh_bl_core.logging.consts import LogLevel
        >>> custom_settings = LoggingConfig()
        >>> custom_settings.console.level = LogLevel.DEBUG
        >>> custom_settings.file.enable = False
        >>> logger_manager = LogManager("service", custom_settings)
        >>> custom_logger = logger_manager.logger
        >>> custom_logger.debug("Отладочная информация")
        >>> # [service] Отладочная информация
        >>>
        >>> # Пример 3: Использование в модуле приложения
        >>> from dh_bl_core.logging import LogManager
        >>>
        >>> class UserService:
        ...     def __init__(self):
        ...         self._logger = LogManager("user_service").logger
        ...
        ...     async def create_user(self, user_data: dict):
        ...         self._logger.info(f"Создание пользователя: {user_data['username']}")
        ...         # Логика создания пользователя
        ...         self._logger.info("Пользователь успешно создан")
    """

    def __init__(self, prefix: str = "", settings: LoggingConfig | None = None):
        """
        Инициализирует менеджер логирования с указанными настройками.

        Создает новый логгер с заданным префиксом и настраивает его согласно
        переданной конфигурации. Удаляет все существующие обработчики логирования
        перед настройкой новых.

        Args:
            prefix (str): Префикс для идентификации источника логов.
                По умолчанию пустая строка.
            settings (LoggingConfig | None): Конфигурация логирования.
                Если не указана, используется конфигурация по умолчанию.

        Examples:
            >>> # Создание менеджера с префиксом
            >>> logger_manager = LogManager("database")
            >>> logger = logger_manager.logger
            >>> logger.info("Подключение к БД")
            >>> # [database] Подключение к БД

            >>> # Создание менеджера с кастомной конфигурацией
            >>> from dh_bl_core.logging.config import LoggingConfig
            >>> from dh_bl_core.logging.consts import LogLevel
            >>> log_settings = LoggingConfig()
            >>> log_settings.console.level = LogLevel.WARNING
            >>> logger_manager = LogManager("security", log_settings)
        """
        self._settings: LoggingConfig = settings or LoggingConfig()
        self._prefix: str = prefix

        logger.remove()

        self._logger = logger.bind(prefix=prefix)
        self._configure_logger()

    @property
    def logger(self):
        """
        Возвращает настроенный экземпляр логгера.

        Предоставляет доступ к логгеру Loguru, который был настроен
        с учетом префикса и конфигурации менеджера.

        Returns:
            Logger: Настроенный экземпляр логгера для записи сообщений.

        Examples:
            >>> logger_manager = LogManager("api")
            >>> logger = logger_manager.logger
            >>> logger.info("Запрос получен")
            >>> # [api] Запрос получен
        """
        return self._logger

    def _configure_logger(self):
        """
        Настраивает обработчики логгера согласно конфигурации.

        Метод добавляет обработчики для вывода логов в консоль и/или файл
        в зависимости от настроек. Уровни логирования, форматы и другие параметры
        берутся из конфигурации менеджера.

        Note:
            Этот метод вызывается автоматически при инициализации менеджера.
            Не предназначен для прямого вызова извне.

        Configuration:
            - Консольный вывод: активируется, если self._settings.console.enable = True
            - Файловый вывод: активируется, если self._settings.file.enable = True

        Examples:
            >>> # Внутреннее использование при создании экземпляра
            >>> logger_manager = LogManager("app")  # _configure_logger вызывается автоматически
        """
        if self._settings.console.enable:
            self.logger.add(
                stdout,
                level=self._settings.console.level,
                colorize=self._settings.console.color,
                format=self._settings.console.format,
            )

        if self._settings.file.enable:
            self.logger.add(
                self._settings.file.path,
                level=self._settings.file.level,
                rotation=self._settings.file.rotation,
                format=self._settings.file.format,
            )

    def apply_new_settings(self, settings: LoggingConfig) -> None:
        """
        Применяет новые настройки логирования во время выполнения.

        Метод позволяет динамически изменять конфигурацию логирования приложения
        без необходимости создания нового экземпляра менеджера. Полностью перенастраивает
        логгер с учетом новых настроек.

        Args:
            settings (LoggingConfig): Новые настройки логирования для применения.

        Note:
            Метод удаляет все существующие обработчики логгера перед применением
            новых настроек, что может привести к потере незаписанных сообщений.
            Рекомендуется использовать с осторожностью в production-среде.

        Examples:
            >>> from dh_bl_core.logging import LogManager
            >>> from dh_bl_core.logging.config import LoggingConfig
            >>> from dh_bl_core.logging.consts import LogLevel
            >>>
            >>> # Создание менеджера с настройками по умолчанию
            >>> logger_manager = LogManager("app")
            >>> logger = logger_manager.logger
            >>> logger.info("Сообщение с настройками по умолчанию")
            >>>
            >>> # Изменение настроек во время выполнения
            >>> new_settings = LoggingConfig()
            >>> new_settings.console.level = LogLevel.WARNING
            >>> new_settings.file.enable = False
            >>> logger_manager.apply_new_settings(new_settings)
            >>> logger.debug("Это сообщение не будет выведено")
            >>> logger.warning("Это сообщение будет выведено")
            >>>
            >>> # Пример динамического изменения уровня логирования
            >>> def toggle_debug_mode(enable: bool):
            ...     new_config = LoggingConfig()
            ...     new_config.console.level = LogLevel.DEBUG if enable else LogLevel.INFO
            ...     logger_manager.apply_new_settings(new_config)
            >>>
            >>> toggle_debug_mode(True)  # Включение отладочного режима
            >>> logger.debug("Отладочная информация включена")
        """
        logger.remove()

        self._settings = settings
        self._configure_logger()
