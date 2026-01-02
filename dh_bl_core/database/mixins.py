# pylint: disable=too-few-public-methods, not-callable
"""Базовые миксины для моделей."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import UUID as PG_UUID
from sqlalchemy import DateTime, func, text
from sqlalchemy.orm import Mapped, mapped_column


class UuidMixin:
    """
    Миксин для добавления UUID поля в модель.

    Добавляет поле uuid с автоматической генерацией значения на уровне базы данных
    с использованием функции gen_random_uuid().

    Attributes:
        uuid (UUID): Уникальный идентификатор сгенерированный PostgreSQL.
                      Поле не может быть NULL.

    Examples:
        >>> from sqlalchemy import create_engine, Column, Integer, String
        >>> from sqlalchemy.orm import sessionmaker
        >>>
        >>> engine = create_engine('postgresql://user:pass@localhost/db')
        >>> SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        >>>
        >>> class User(Base, UuidMixin):
        ...     __tablename__ = 'users'
        ...     id = Column(Integer, primary_key=True)
        ...     name = Column(String, nullable=False)
        >>>
        >>> # При создании пользователя поле uuid будет автоматически сгенерировано
        >>> db = SessionLocal()
        >>> user = User(name='John')
        >>> db.add(user)
        >>> db.commit()
        >>> print(user.uuid)
        d7e5b9a4-1c4f-4a2a-8b1c-3d5e6f7a8b9c
    """

    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), server_default=text("gen_random_uuid()"), nullable=False)


class TimestampMixin:
    """
    Миксин для добавления временных меток в модель.

    Добавляет поля created_at и updated_at для отслеживания времени создания
    и последнего обновления записи. Поле updated_at автоматически обновляется
    при каждом изменении записи.

    Attributes:
        created_at (datetime): Время создания записи. Устанавливается один раз при создании.
        updated_at (datetime): Время последнего обновления записи. Обновляется автоматически
                             при каждом изменении записи.

    Properties:
        is_created (bool): Возвращает True, если запись только что создана (created_at == updated_at),
                           False если запись была обновлена.

    Examples:
        >>> from sqlalchemy import create_engine, Column, Integer, String
        >>> from sqlalchemy.orm import sessionmaker
        >>>
        >>> engine = create_engine('postgresql://user:pass@localhost/db')
        >>> SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        >>>
        >>> class Post(Base, TimestampMixin):
        ...     __tablename__ = 'posts'
        ...     id = Column(Integer, primary_key=True)
        ...     title = Column(String, nullable=False)
        >>>
        >>> db = SessionLocal()
        >>> post = Post(title='Hello World')
        >>> db.add(post)
        >>> db.commit()
        >>>
        >>> # После создания created_at и updated_at совпадают
        >>> print(post.is_created)
        True
        >>>
        >>> # После обновления записи
        >>> post.title = 'Updated Title'
        >>> db.commit()
        >>> print(post.is_created)
        False
        >>> print(post.updated_at > post.created_at)
        True
    """

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    @property
    def is_created(self) -> bool:
        """
        Проверяет, была ли запись только что создана.

        Сравнивает время создания и время последнего обновления записи.
        Запись считается новой, если эти временные метки совпадают.

        Returns:
            bool: True если запись только что создана (created_at == updated_at),
                  False если запись была обновлена после создания.

        Examples:
            >>> post = Post(title='New Post')
            >>> db.add(post)
            >>> db.commit()
            >>> print(post.is_created)
            True
            >>>
            >>> post.title = 'Updated Title'
            >>> db.commit()
            >>> print(post.is_created)
            False
        """
        return self.created_at == self.updated_at


class SoftDeleteMixin:
    """
    Миксин для реализации мягкого удаления.

    Добавляет поле deleted_at для пометки записи как удаленной без фактического
    удаления из базы данных. Это позволяет восстановить запись при необходимости.

    Attributes:
        deleted_at (datetime | None): Время удаления записи. None если запись не удалена.

    Properties:
        is_deleted (bool): Возвращает True если запись помечена как удаленная (deleted_at не None),
                          False если запись активна.

    Examples:
        >>> from sqlalchemy import create_engine, Column, Integer, String
        >>> from sqlalchemy.orm import sessionmaker
        >>>
        >>> engine = create_engine('postgresql://user:pass@localhost/db')
        >>> SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        >>>
        >>> class Document(Base, SoftDeleteMixin):
        ...     __tablename__ = 'documents'
        ...     id = Column(Integer, primary_key=True)
        ...     name = Column(String, nullable=False)
        >>>
        >>> db = SessionLocal()
        >>> doc = Document(name='Report')
        >>> db.add(doc)
        >>> db.commit()
        >>>
        >>> # Проверка состояния удаления
        >>> print(doc.is_deleted)
        False
        >>>
        >>> # Помечаем документ как удаленный
        >>> doc.deleted_at = datetime.utcnow()
        >>> db.commit()
        >>> print(doc.is_deleted)
        True
        >>>
        >>> # Восстановление документа
        >>> doc.deleted_at = None
        >>> db.commit()
        >>> print(doc.is_deleted)
        False
    """

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)

    @property
    def is_deleted(self) -> bool:
        """
        Проверяет, была ли запись помечена как удаленная.

        Проверяет наличие временной метки удаления. Если поле deleted_at
        содержит значение (не None), запись считается удаленной.

        Returns:
            bool: True если запись помечена как удаленная (deleted_at не None),
                  False если запись активна (deleted_at is None).

        Examples:
            >>> doc = Document(name='Report')
            >>> db.add(doc)
            >>> db.commit()
            >>> print(doc.is_deleted)
            False
            >>>
            >>> doc.deleted_at = datetime.utcnow()
            >>> db.commit()
            >>> print(doc.is_deleted)
            True
        """
        return self.deleted_at is not None


class DeactivateMixin:
    """
    Миксин для реализации деактивации записи.

    Добавляет поле deactivated_at для пометки записи как деактивированной.
    В отличие от мягкого удаления, деактивация может иметь другую семантику
    в бизнес-логике приложения (например, временная блокировка пользователя).

    Attributes:
        deactivated_at (datetime | None): Время деактивации записи. None если запись активна.

    Properties:
        is_deactivated (bool): Возвращает True если запись деактивирована (deactivated_at не None),
                             False если запись активна.

    Examples:
        >>> from sqlalchemy import create_engine, Integer, String
        >>> from sqlalchemy.orm import sessionmaker
        >>>
        >>> engine = create_engine('postgresql://user:pass@localhost/db')
        >>> SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        >>>
        >>> class User(Base, DeactivateMixin):
        ...     __tablename__ = 'users'
        ...     id = Column(Integer, primary_key=True)
        ...     username = Column(String, nullable=False)
        >>>
        >>> db = SessionLocal()
        >>> user = User(username='john_doe')
        >>> db.add(user)
        >>> db.commit()
        >>>
        >>> # Проверка состояния активности
        >>> print(user.is_deactivated)
        False
        >>>
        >>> # Деактивация пользователя
        >>> user.deactivated_at = datetime.utcnow()
        >>> db.commit()
        >>> print(user.is_deactivated)
        True
        >>>
        >>> # Реактивация пользователя
        >>> user.deactivated_at = None
        >>> db.commit()
        >>> print(user.is_deactivated)
        False
    """

    deactivated_at: Mapped[datetime | None] = mapped_column(DateTime)

    @property
    def is_deactivated(self) -> bool:
        """
        Проверяет, была ли запись деактивирована.

        Проверяет наличие временной метки деактивации. Если поле deactivated_at
        содержит значение (не None), запись считается деактивированной.

        Returns:
            bool: True если запись деактивирована (deactivated_at не None),
                  False если запись активна (deactivated_at is None).

        Examples:
            >>> user = User(username='john_doe')
            >>> db.add(user)
            >>> db.commit()
            >>> print(user.is_deactivated)
            False
            >>>
            >>> user.deactivated_at = datetime.utcnow()
            >>> db.commit()
            >>> print(user.is_deactivated)
            True
        """
        return self.deactivated_at is not None
