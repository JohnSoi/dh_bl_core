# pylint: disable=unnecessary-ellipsis
"""Типизация для работы БД."""
from typing import Protocol


class DbSettingProtocol(Protocol):
    """
    Протокол, определяющий интерфейс для настроек подключения к базе данных.

    Этот протокол используется для аннотации типов и определяет необходимые атрибуты
    и методы, которые должны быть реализованы в классах настроек базы данных.

    Attributes:
        echo (bool): Флаг, указывающий, нужно ли выводить SQL-запросы в лог.
                     Если True, все SQL-запросы будут логироваться.

    Examples:
        >>> # Пример 1: Реализация протокола в пользовательском классе
        >>> class PostgresSettings:
        ...     echo: bool = True
        ...
        ...     def get_sync_connection_url(self) -> str:
        ...         return "postgresql://user:password@localhost:5432/dbname"
        ...
        ...     def get_async_connection_url(self) -> str:
        ...         return "postgresql+asyncpg://user:password@localhost:5432/dbname"

        >>> # Пример 2: Использование протокола для аннотации типов
        >>> def create_database_engine(settings: DbSettingProtocol):
        ...     '''Создает движок базы данных на основе настроек'''
        ...     if settings.echo:
        ...         print(f"SQL логирование включено: {settings.get_sync_connection_url()}")
        ...     return settings.get_async_connection_url()

        >>> # Пример 3: Проверка соответствия класса протоколу
        >>> settings = PostgresSettings()
        >>> isinstance(settings, DbSettingProtocol)
        True
        >>> create_database_engine(settings)
        'postgresql+asyncpg://user:password@localhost:5432/dbname'
    """

    echo: bool

    def get_sync_connection_url(self) -> str:
        """
        Возвращает синхронный URL для подключения к базе данных.

        Используется для синхронных драйверов подключения, таких как psycopg2.
        Формат URL: dialect://user:password@host:port/database

        Returns:
            str: Синхронный URL подключения к базе данных

        Examples:
            >>> settings = PostgresSettings()
            >>> url = settings.get_sync_connection_url()
            >>> print(url)
            postgresql://user:password@localhost:5432/dbname

            >>> # Использование URL для создания синхронного подключения
            >>> from sqlalchemy import create_engine
            >>> engine = create_engine(url, echo=settings.echo)
        """
        ...

    def get_async_connection_url(self) -> str:
        """
        Возвращает асинхронный URL для подключения к базе данных.

        Используется для асинхронных драйверов подключения, таких как asyncpg.
        Формат URL: dialect+driver://user:password@host:port/database

        Returns:
            str: Асинхронный URL подключения к базе данных

        Examples:
            >>> settings = PostgresSettings()
            >>> url = settings.get_async_connection_url()
            >>> print(url)
            postgresql+asyncpg://user:password@localhost:5432/dbname

            >>> # Использование URL для создания асинхронного подключения
            >>> from sqlalchemy.ext.asyncio import create_async_engine
            >>> engine = create_async_engine(url, echo=settings.echo)
        """
        ...
