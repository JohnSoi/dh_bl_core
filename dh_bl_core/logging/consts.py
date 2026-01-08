"""Константы для логирования."""

from enum import StrEnum


class LogLevel(StrEnum):
    """
    Уровни логирования приложения.

    Этот класс определяет доступные уровни логирования, которые могут использоваться
    для фильтрации и классификации сообщений в системе логирования. Уровни соответствуют
    стандартным уровням логирования и представлены как строковые значения.

    Attributes:
        DEBUG (str): Подробная отладочная информация, полезная при разработке и диагностике.
        INFO (str): Общая информация о ходе выполнения программы.
        WARNING (str): Предупреждение о потенциально нежелательном событии.
        ERROR (str): Ошибка, которая не привела к остановке программы.
        CRITICAL (str): Критическая ошибка, которая может привести к остановке программы.

    Examples:
        >>> # Использование уровней логирования
        >>> from dh_bl_core.logging.consts import LogLevel
        >>>
        >>> # Проверка значений уровней
        >>> print(LogLevel.DEBUG)
        DEBUG
        >>> print(LogLevel.ERROR)
        ERROR
        >>>
        >>> # Использование в конфигурации
        >>> console_level = LogLevel.DEBUG
        >>> file_level = LogLevel.INFO
        >>>
        >>> # Сравнение уровней
        >>> LogLevel.WARNING > LogLevel.INFO
        True
        >>> LogLevel.DEBUG < LogLevel.INFO
        True
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class LogFormat(StrEnum):
    """
    Форматы сообщений логов для разных целей вывода.

    Этот класс определяет форматы сообщений логов для различных целей вывода:
    консоль и файл. Форматы используют синтаксис Loguru для форматирования сообщений.

    Attributes:
        CONSOLE (str): Формат для вывода в консоль с цветовой подсветкой.
            Включает префикс, время в зеленом цвете и сообщение с цветом уровня.
        FILE (str): Формат для записи в файл. Включает уровень, префикс,
            время в скобках и сообщение. Подходит для последующего анализа.

    Examples:
        >>> # Использование форматов логирования
        >>> from dh_bl_core.logging.consts import LogFormat
        >>>
        >>> # Получение формата для консоли
        >>> console_format = LogFormat.CONSOLE
        >>> print(console_format)
        extra[prefix] <green>{time}</green> <level>{message}</level>
        >>>
        >>> # Получение формата для файла
        >>> file_format = LogFormat.FILE
        >>> print(file_format)
        [{level}][{extra[prefix]}] ({time}): {message}
        >>>
        >>> # Использование в конфигурации
        >>> from dh_bl_core.logging.config import ConsoleConfig, FileConfig
        >>> console_config = ConsoleConfig()
        >>> console_config.format = LogFormat.CONSOLE
        >>> file_config = FileConfig()
        >>> file_config.format = LogFormat.FILE
    """

    CONSOLE = "extra[prefix] <green>{time}</green> <level>{message}</level>"
    FILE = "[{level}][{extra[prefix]}] ({time}): {message}"


# Путь к файлу логов
LOG_FILE_PATH: str = "logs/{time}.log"
# Размер файла логов
LOG_FILE_ROTATION_SIZE: str = "100 MB"
