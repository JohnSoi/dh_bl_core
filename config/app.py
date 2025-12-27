"""Модуль конфигурации приложения."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.validators import validate_app_version


class AppConfig(BaseSettings):
    """
    Класс для хранения и управления конфигурацией приложения.

    AppConfig наследует от BaseSettings из Pydantic и предоставляет централизованное
    хранилище для всех настроек приложения. Класс автоматически загружает значения
    из переменных окружения с префиксом 'APP_' из файла .env-example, расположенного
    в корне проекта.

    Attributes:
        debug (bool): Режим отладки. Определяет, включен ли режим отладки.
            Значение по умолчанию: False. Загружается из переменной APP_DEBUG.
        name (str): Название приложения. Используется для идентификации и отображения.
            Загружается из переменной APP_NAME.
        version (str): Версия приложения в формате YEAR.MONTH.PATCH.
            Загружается из переменной APP_VERSION.

    Examples:
        >>> from dh_bl_core.config import AppConfig
        >>>
        >>> config = AppConfig()
        >>> print(f"Запуск {config.name} версии {config.version}")
        Запуск MyApp версии 1.0.0
        >>> if config.debug:
        ...     print("Режим отладки включен")
    """

    model_config = SettingsConfigDict(env_file=".env-example", env_prefix="APP_")

    debug: bool = False
    name: str
    version: str

    @field_validator("version")
    @classmethod
    def validate_version_format(cls, v: str) -> str:
        """
        Валидирует формат версии в формате YEAR.MONTH.PATCH.

        Проверяет, что версия соответствует формату YYYY.MM.PATCH, где:
        - YYYY - четырехзначный год (например, 2025, 2026)
        - MM - номер месяца от 01 до 12
        - PATCH - номер патча (целое число)

        Args:
            v (str): Строка с версией для проверки

        Returns:
            str: Возвращается исходная строка, если валидация прошла успешно

        Raises:
            InvalidVersionFormatException: Если формат версии некорректен
                (не соответствует шаблону YEAR.MONTH.PATCH)
            InvalidVersionYearException: Если год в версии выходит за допустимый диапазон
                (меньше VERSION_MIN_YEAR или больше текущего года + 1)
            InvalidVersionMonthException: Если месяц в версии выходит за допустимый диапазон
                (меньше MIN_VERSION_MONTH или больше MAX_VERSION_MONTH)


        Examples:
            >>> AppConfig.validate_version_format("2025.12.1")
            '2025.12.1'
            >>> AppConfig.validate_version_format("2026.01.5")
            '2026.01.5'
            >>> AppConfig.validate_version_format("23.12.1")
            Traceback (most recent call last):
            ...
            ValueError: Версия должна быть в формате YEAR.MONTH.PATCH (например, 2023.12.1)
        """
        return validate_app_version(v)


@lru_cache()
def get_app_config() -> AppConfig:
    """
    Возвращает объект конфигурации приложения.

    Эта функция использует lru_cache для хранения и повторного использования
    объекта конфигурации. Это позволяет оптимизировать производительность,
    так как создание объекта конфигурации занимает время.

    Examples:
        >>> from pydantic_settings import BaseSettings
        >>> from dh_bl_core.config import get_app_config, AppConfig
        >>>
        >>> config: AppConfig = get_app_config()
        >>> print(f"Запуск {config.name} версии {config.version}")
        Запуск MyApp версии 1.0.0
        >>> class Config(BaseSettings)
        >>>     # Базовые настройки приложения
        >>>     app_settings: AppConfig = get_app_config()
        >>>
    """
    return AppConfig() # pyright: ignore[reportCallIssue]
