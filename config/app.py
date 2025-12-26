"""Модуль конфигурации приложения."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """
    Класс для хранения и управления конфигурацией приложения.

    AppConfig наследует от BaseSettings из Pydantic и предоставляет централизованное
    хранилище для всех настроек приложения. Класс автоматически загружает значения
    из переменных окружения с префиксом 'APP_' из файла .env, расположенного
    в корне проекта.

    Attributes:
        debug (bool): Режим отладки. Определяет, включен ли режим отладки.
            Значение по умолчанию: False. Загружается из переменной APP_DEBUG.
        name (str): Название приложения. Используется для идентификации и отображения.
            Загружается из переменной APP_NAME.
        version (str): Версия приложения в формате YEAR.MONTH.PATCH.
            Загружается из переменной APP_VERSION.

    Examples:
        >>> from config.app import AppConfig
        >>> config = AppConfig()
        >>> print(f"Запуск {config.name} версии {config.version}")
        Запуск MyApp версии 1.0.0
        >>> if config.debug:
        ...     print("Режим отладки включен")
    """
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")

    debug: bool = False
    name: str
    version: str


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
    return AppConfig()
