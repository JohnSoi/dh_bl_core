# pylint: disable=broad-exception-caught
"""Менеджер подключения к базе данных."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from .exceptions import DbMangerNotInit
from .types import DbSettingProtocol


class AsyncDatabaseConnectionManager:
    """
    Менеджер соединения с базой данных, реализующий паттерн Singleton.

    Этот класс управляет подключением к базе данных, создает движки и фабрики сессий,
    а также предоставляет контекстные менеджеры для работы с сессиями.

    Attributes:
        _instance (Optional[AsyncDatabaseConnectionManager]):
            Статический экземпляр класса для реализации паттерна Singleton.
        _engine (Optional[AsyncEngine]): Движок SQLAlchemy для подключения к БД.
        _session_maker (Optional[async_sessionmaker]): Фабрика сессий SQLAlchemy.

    Examples:
        >>> # Пример 1: Инициализация менеджера и получение сессии
        >>> from dh_bl_core.database import db_manager
        >>> from settings import DatabaseSettings
        >>>
        >>> # Инициализация менеджера с настройками
        >>> db_manager.init(DatabaseSettings())
        >>>
        >>> # Получение сессии через генератор
        >>> async for session in db_manager.get_session():
        ...     result = await session.execute("SELECT * FROM users")
        ...     users = result.fetchall()

        >>> # Пример 2: Использование контекстного менеджера
        >>> async with db_manager.get_db_context() as session:
        ...     result = await session.execute("SELECT * FROM users")
        ...     users = result.fetchall()
        ...     await session.commit()

        >>> # Пример 3: Проверка работоспособности подключения
        >>> is_healthy = await db_manager.health_check()
        >>> print(f"Состояние БД: {'работает' if is_healthy else 'недоступна'}")
    """

    _instance: Optional["AsyncDatabaseConnectionManager"] = None
    _engine: AsyncEngine | None = None
    _session_maker: async_sessionmaker | None = None

    def __new__(cls):
        """
        Реализация паттерна Singleton.

        Гарантирует, что будет существовать только один экземпляр менеджера соединения с БД.

        Returns:
            AsyncDatabaseConnectionManager: Единственный экземпляр класса
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def init(self, db_settings: DbSettingProtocol) -> None:
        """
        Инициализирует менеджер соединения с базой данных.

        Создает движок SQLAlchemy и фабрику сессий на основе переданных настроек.
        Поддерживает как синхронный, так и асинхронный режимы работы.

        Args:
            db_settings (DbSettingProtocol): Настройки подключения к базе данных,
                реализующие протокол DbSettingProtocol.

        Notes:
            Если менеджер уже был инициализирован, метод ничего не делает.
            Для повторной инициализации необходимо сначала вызвать метод close().

        Examples:
            >>> # Инициализация в асинхронном режиме
            >>> db_manager.init(settings)
            >>>
            >>> # Инициализация в приложении FastAPI
            >>> from dh_bl_core.config import get_pg_database_config, get_app_config
            >>> @asynccontextmanager
            >>> async def lifespan(app: FastAPI):
            ...     # Старт приложения
            ...     print("🚀 Starting application...")
            ...
            ...     # Инициализация БД
            ...     settings = get_pg_database_config()
            ...     db_manager.init(settings)
            ...
            ...     # Проверка соединения с БД
            ...     is_healthy = await db_manager.health_check()
            ...     if not is_healthy:
            ...         print("⚠️  Database connection failed!")
            ...     else:
            ...         print("✅ Database connected successfully")
            ...
            ...     yield  # Приложение запущено
            ...
            ...     # Завершение работы
            ...     print("🛑 Shutting down application...")
            ...     await db_manager.close()
            ...     print("✅ Database connections closed")
            >>>
            >>>
            >>> # Создание FastAPI приложения
            >>> app = FastAPI(
            ...     title=get_app_config().APP_NAME,
            ...     version="1.0.0",
            ...     lifespan=lifespan
            >>> )
        """
        # Мы уже инициализировали соединение - выходим
        if self._engine is not None:
            return

        database_url: str = db_settings.get_async_connection_url()

        self._engine = create_async_engine(url=database_url, echo=db_settings.echo)
        self._session_maker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        """
        Возвращает движок SQLAlchemy для подключения к базе данных.

        Raises:
            DbMangerNotInit: Если менеджер не был инициализирован методом init().

        Returns:
            AsyncEngine: Движок SQLAlchemy (асинхронный или синхронный).

        Examples:
            >>> # Получение движка для прямого подключения
            >>> engine = db_manager.engine
            >>>
            >>> # Использование движка для выполнения сырого SQL
            >>> async with engine.connect() as conn:
            ...     result = await conn.execute("SELECT 1")
            ...     print(await result.scalar())
        """
        if self._engine is None:
            raise DbMangerNotInit()

        return self._engine

    @property
    def session_maker(self) -> async_sessionmaker | sessionmaker:
        """
        Возвращает фабрику сессий SQLAlchemy.

        Создает сессии для взаимодействия с базой данных через ORM.

        Raises:
            DbMangerNotInit: Если менеджер не был инициализирован методом init().

        Returns:
            async_sessionmaker | sessionmaker: Фабрика сессий SQLAlchemy.

        Examples:
            >>> # Создание новой сессии
            >>> SessionLocal = db_manager.session_maker
            >>> session = SessionLocal()
            >>> try:
            ...     result = await session.execute("SELECT * FROM users")
            ...     users = result.fetchall()
            ... finally:
            ...     await session.close()
        """
        if self._session_maker is None:
            raise DbMangerNotInit()

        return self._session_maker

    async def get_session(self) -> AsyncGenerator[AsyncSession | Session]:
        """
        Генератор сессий для использования в FastAPI зависимостях.

        Предоставляет асинхронную сессию для работы с базой данных.
        Сессия автоматически закрывается после выхода из контекста.

        Yields:
            AsyncSession | Session: Асинхронная сессия SQLAlchemy.

        Raises:
            DbMangerNotInit: Если менеджер не был инициализирован.

        Examples:
            >>> # Использование в FastAPI зависимости
            >>> from fastapi import Depends
            >>>
            >>> async def get_db_session(session = Depends(db_manager.get_session)):
            ...     return session
            >>>
            >>> # Прямое использование в корутине
            >>> async for session in db_manager.get_session():
            ...     result = await session.execute("SELECT * FROM users")
            ...     users = result.fetchall()
        """
        async with self.session_maker() as session:
            yield session

    async def close(self) -> None:
        """
        Закрывает соединение с базой данных.

        Освобождает ресурсы, закрывает пул соединений и завершает работу движка.
        Может быть использован при остановке приложения или для переключения
        между разными базами данных.

        Examples:
            >>> # Закрытие соединения при остановке приложения
            >>> await db_manager.close()
            >>>
            >>> # Переключение между разными базами данных
            >>> await db_manager.close()  # Закрываем текущее соединение
            >>> db_manager.init(new_settings, async_mode=True)  # Инициализируем с новыми настройками
        """
        if self._engine is None:
            return

        await self._engine.dispose()

    async def health_check(self) -> bool:
        """
        Проверяет работоспособность подключения к базе данных.

        Выполняет простой запрос к базе данных для проверки соединения.

        Returns:
            bool: True, если база данных доступна и отвечает на запросы, False в противном случае.

        Examples:
            >>> # Проверка состояния базы данных
            >>> is_healthy = await db_manager.health_check()
            >>> if is_healthy:
            ...     print("База данных работает нормально")
            ... else:
            ...     print("База данных недоступна")

            >>> # Использование в health-check эндпоинте API
            >>> @app.get("/health")
            ... async def health_check():
            ...     return {"database": "healthy" if await db_manager.health_check() else "unhealthy"}
        """
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))

            return True
        except Exception:
            return False

    @asynccontextmanager
    async def get_db_context(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Контекстный менеджер для работы с сессией базы данных.

        Предоставляет сессию с автоматическим управлением транзакциями:
        - При возникновении исключения выполняется rollback
        - Сессия автоматически закрывается при выходе из контекста
        - При успешном выполнении можно вручную вызвать commit()

        Yields:
            AsyncSession: Асинхронная сессия SQLAlchemy.

        Raises:
            DbMangerNotInit: Если менеджер не был инициализирован.
            Exception: Любое исключение, возникшее при работе с базой данных,
                      после выполнения rollback.

        Examples:
            >>> # Использование в сервисном слое
            >>> async def create_user(user_data: dict):
            ...     async with db_manager.get_db_context() as session:
            ...         session.add(User(**user_data))
            ...         await session.commit()
            ...         return user_data
            >>>
            >>> # Работа с транзакциями
            >>> async with db_manager.get_db_context() as session:
            ...     try:
            ...         session.add(User(name="John"))
            ...         session.add(Order(user_id=1))
            ...         await session.commit()  # Явная фиксация изменений
            ...     except Exception as e:
            ...         # При исключении автоматически выполнится rollback
            ...         print(f"Ошибка при сохранении: {e}")
        """
        session = self.session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Глобальный экземпляр менеджера для использования в приложении
db_manager = AsyncDatabaseConnectionManager()
