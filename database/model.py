# pylint: disable=too-few-public-methods
"""
Модуль базовой модели для SQLAlchemy.

Содержит базовую модель, от которой наследуются все остальные модели в приложении.
Обеспечивает автоматическое преобразование имени класса в snake_case для имени таблицы
и предоставляет базовый первичный ключ.
"""

from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

from utils import camel_to_snake_case

# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()


class BaseModel(Base):
    """
    Абстрактная базовая модель для всех моделей приложения.

    Наследуется от SQLAlchemy declarative base и служит родительским классом
    для всех моделей в приложении. Обеспечивает общую функциональность:

    - Автоматическое преобразование имени класса в snake_case для имени таблицы
    - Единый формат первичного ключа
    - Абстрактный класс (не создает таблицу в БД)

    Attributes:
        id (int): Автоинкрементный первичный ключ. Уникальный идентификатор записи.

    Examples:
        >>> from sqlalchemy import String, Column, Integer
        >>>
        >>> class User(BaseModel):
        ...     __tablename__ = 'users'  # Будет автоматически определено как 'user'
        ...     username = Column(String(50), nullable=False)
        ...     email = Column(String(100), nullable=False, unique=True)
        >>>
        >>> class Product(BaseModel):
        ...     __tablename__ = 'products'  # Будет автоматически определено как 'product'
        ...     name = Column(String(100), nullable=False)
        ...     price = Column(Integer, nullable=False)
        >>>
        >>> # При создании таблиц в базе данных
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine('sqlite:///example.db')
        >>> Base.metadata.create_all(engine)
        >>>
        >>> # В результате будут созданы таблицы 'user' и 'product'
        >>> # с единым форматом первичного ключа
    """

    __abstract__ = True

    @classmethod
    def __tablename__(cls):
        """
        Автоматически генерирует имя таблицы из имени класса.

        Преобразует имя класса из CamelCase в snake_case с помощью утилиты
        camel_to_snake_case. Например, класс UserAccount будет преобразован
        в имя таблицы 'user_account'.

        Returns:
            str: Имя таблицы в формате snake_case.

        Examples:
            >>> class UserAccount(BaseModel):
            ...     pass
            >>> UserAccount.__tablename__()
            'user_account'
            >>>
            >>> class APIKey(BaseModel):
            ...     pass
            >>> APIKey.__tablename__()
            'api_key'
        """
        return camel_to_snake_case(cls.__name__)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
