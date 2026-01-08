"""Конфигурация логирования."""

from pydantic_settings import BaseSettings, SettingsConfigDict

from .consts import LOG_FILE_PATH, LOG_FILE_ROTATION_SIZE, LogFormat, LogLevel


class ConsoleConfig(BaseSettings):
    """
    Конфигурация для консольного вывода логов.

    Этот класс определяет настройки вывода логов в консоль, включая уровень логирования,
    цветовой вывод и формат сообщений. Настройки могут быть переопределены через переменные
    окружения с префиксом LOG_CONSOLE_.

    Attributes:
        enable (bool): Флаг включения консольного вывода. По умолчанию равен
            значению debug из конфигурации приложения.
        color (bool): Флаг использования цветового оформления логов. По умолчанию True.
        level (LogLevel): Уровень логирования для консоли. По умолчанию DEBUG.
        format (LogFormat): Формат сообщений лога для консоли. По умолчанию CONSOLE.

    Examples:
        >>> # Создание конфигурации с настройками по умолчанию
        >>> console_config = ConsoleConfig()
        >>> print(console_config.enable)
        True
        >>>
        >>> # Переопределение настроек
        >>> custom_console = ConsoleConfig(
        ...     enable=True,
        ...     color=False,
        ...     level=LogLevel.INFO,
        ...     format=LogFormat.SIMPLE
        ... )
        >>>
        >>> # Использование в конфигурации логирования
        >>> from dh_bl_core.logging.config import LoggingConfig
        >>> logging_config = LoggingConfig()
        >>> console_settings = logging_config.console
        >>> print(f"Уровень логирования: {console_settings.level}")
        Уровень логирования: LogLevel.INFO
    """

    model_config = SettingsConfigDict(env_file=".env", env_prefix="LOG_CONSOLE_", extra="allow")

    enable: bool = False
    color: bool = True
    level: LogLevel = LogLevel.DEBUG
    format: LogFormat = LogFormat.CONSOLE


class FileConfig(BaseSettings):
    """
    Конфигурация для файлового вывода логов.

    Этот класс определяет настройки записи логов в файл, включая путь к файлу,
    размер ротации, формат сообщений и уровень логирования. Настройки могут быть
    переопределены через переменные окружения с префиксом LOG_FILE_.

    Attributes:
        enable (bool): Флаг включения файлового вывода. По умолчанию True.
        path (str): Путь к файлу логов. По умолчанию значение из констант.
        rotation (str): Размер файла при достижении которого происходит ротация.
            По умолчанию значение из констант.
        format (LogFormat): Формат сообщений лога для файла. По умолчанию FILE.
        level (LogLevel): Уровень логирования для файла. По умолчанию INFO.

    Examples:
        >>> # Создание конфигурации с настройками по умолчанию
        >>> file_config = FileConfig()
        >>> print(file_config.enable)
        True
        >>>
        >>> # Переопределение настроек
        >>> custom_file = FileConfig(
        ...     enable=True,
        ...     path="/var/log/app.log",
        ...     rotation="100 MB",
        ...     format=LogFormat.JSON,
        ...     level=LogLevel.WARNING
        ... )
        >>>
        >>> # Использование в конфигурации логирования
        >>> from dh_bl_core.logging.config import LoggingConfig
        >>> logging_config = LoggingConfig()
        >>> file_settings = logging_config.file
        >>> print(f"Файл логов: {file_settings.path}")
        Файл логов: logs/app.log
    """

    model_config = SettingsConfigDict(env_file=".env", env_prefix="LOG_FILE_", extra="allow")

    enable: bool = True
    path: str = LOG_FILE_PATH
    rotation: str = LOG_FILE_ROTATION_SIZE
    format: LogFormat = LogFormat.FILE
    level: LogLevel = LogLevel.INFO


class LoggingConfig(BaseSettings):
    """
    Основная конфигурация логирования приложения.

    Этот класс объединяет конфигурации для консольного и файлового вывода логов.
    Настройки могут быть переопределены через переменные окружения с префиксом LOG_.
    Предоставляет централизованный доступ к настройкам логирования всего приложения.

    Attributes:
        console (ConsoleConfig): Конфигурация для консольного вывода логов.
        file (FileConfig): Конфигурация для файлового вывода логов.

    Examples:
        >>> # Создание конфигурации по умолчанию
        >>> logging_config = LoggingConfig()
        >>> print(f"Консоль включена: {logging_config.console.enable}")
        Консоль включена: True
        >>> print(f"Файл логов: {logging_config.file.path}")
        Файл логов: logs/app.log
        >>>
        >>> # Доступ к вложенным настройкам
        >>> console_level = logging_config.console.level
        >>> file_level = logging_config.file.level
        >>> print(f"Уровни логирования: консоль={console_level}, файл={file_level}")
        Уровни логирования: консоль=LogLevel.DEBUG, файл=LogLevel.INFO
        >>>
        >>> # Использование в коде приложения
        >>> from dh_bl_core.logging.config import LoggingConfig
        >>> from dh_bl_core.logging.manager import LogManager
        >>>
        >>> # Получение конфигурации
        >>> config = LoggingConfig()
        >>> # Создание менеджера логирования с кастомной конфигурацией
        >>> logger_manager = LogManager("app", config)
    """

    model_config = SettingsConfigDict(env_file=".env", env_prefix="LOG_", extra="allow")

    console: ConsoleConfig = ConsoleConfig()
    file: FileConfig = FileConfig()
