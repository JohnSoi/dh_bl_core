"""Модуль конфигурации подключения к базе данных PostgreSQL."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from . import validators


class PGDatabaseConfig(BaseSettings):
    """
    Класс для хранения и управления конфигурацией подключения к базе данных PostgreSQL.

    PGDatabaseConfig наследует от BaseSettings из Pydantic и предоставляет
    централизованное хранилище для всех настроек подключения к базе данных.
    Класс автоматически загружает значения из переменных окружения с префиксом
    'DB_' из файла .env-example, расположенного в корне проекта.

    Attributes:
        host (str): Хост базы данных. По умолчанию 'localhost'.
        port (int): Порт базы данных. По умолчанию 5432 (PostgreSQL).
        username (str): Имя пользователя для подключения к базе данных.
        password (str): Пароль для подключения к базе данных.
        database (str): Название базы данных.

    Examples:
        >>> from dh_bl_core.config import PGDatabaseConfig
        >>>
        >>> # Создание конфигурации из переменных окружения
        >>> config = PGDatabaseConfig()
        >>>
        >>> # Получение строки подключения
        >>> sync_url = config.get_sync_connection_url()
        >>> async_url = config.get_async_connection_url()
        >>> print(sync_url)
        postgresql://user:password@localhost:5432/dbname
    """
    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_")

    host: str = "localhost"
    port: int = 5432
    username: str
    password: str
    database: str

    @field_validator("host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        """
        Валидирует хост базы данных.

        Args:
            v (str): Хост для проверки

        Returns:
            str: Возвращается исходная строка, если валидация прошла успешно

        Raises:
            InvalidDbHostException: Если хост пустой или задан не строкой
        """
        return validators.validate_db_host(v)
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """
        Валидирует имя пользователя базы данных.

        Args:
            v (str): Имя пользователя для проверки

        Returns:
            str: Возвращается исходная строка, если валидация прошла успешно

        Raises:
            InvalidUserNameException: Если имя пользователя пустое
        """
        return validators.validate_db_username(v)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Валидирует пароль базы данных.

        Args:
            v (str): Пароль для проверки

        Returns:
            str: Возвращается исходная строка, если валидация прошла успешно

        Raises:
            InvalidDbPasswordException: Если пароль пустой
        """
        return validators.validate_db_password(v)
    
    @field_validator("database")
    @classmethod
    def validate_database(cls, v: str) -> str:
        """
        Валидирует название базы данных.

        Args:
            v (str): Название базы данных для проверки

        Returns:
            str: Возвращается исходная строка, если валидация прошла успешно

        Raises:
            InvalidDbNameException: Если название базы данных пустое
        """
        return validators.validate_db_name(v)
    
    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """
        Валидирует порт базы данных.

        Args:
            v (int): Порт для проверки

        Returns:
            int: Возвращается исходное значение, если валидация прошла успешно

        Raises:
            InvalidDbPortException: Если порт вне допустимого диапазона (1-65535)
        """
        return validators.validate_db_port(v)
    
    def get_sync_connection_url(self) -> str:
        """
        Генерирует строку подключения для синхронного драйвера.

        Returns:
            str: Строка подключения в формате driver://username:password@host:port/database

        Examples:
            >>> config = PGDatabaseConfig(
            ...     host="localhost",
            ...     port=5432,
            ...     username="user",
            ...     password="pass",
            ...     database="mydb"
            ... )
            >>> config.get_sync_connection_url()
            'postgresql://user:pass@localhost:5432/mydb'
        """
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def get_async_connection_url(self) -> str:
        """
        Генерирует строку подключения для асинхронного драйвера.

        Returns:
            str: Строка подключения в формате driver://username:password@host:port/database

        Examples:
            >>> config = PGDatabaseConfig(
            ...     host="localhost",
            ...     port=5432,
            ...     username="user",
            ...     password="pass",
            ...     database="mydb"
            ... )
            >>> config.get_async_connection_url()
            'postgresql+asyncpg://user:pass@localhost:5432/mydb'
        """
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"