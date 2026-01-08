"""Модуль валидаторов для конфигураций."""

from typing import Type

from dh_bl_core.exceptions import BaseAppException
from dh_bl_core.validators import (
    ValueIsEmptyStrException,
    ValueIsNotIntException,
    ValueIsNotStrException,
    validate_is_int,
    validate_is_not_empty_str,
)

from . import exceptions as exc
from .consts import MAX_PORT_NUMBER, MIN_PORT_NUMBER


def validate_db_host(host: str) -> str:
    """
    Валидирует хост базы данных.

    Проверяет, что хост базы данных не является пустой строкой.

    Используется как валидатор в классе DatabaseConfig.

    Args:
        host (str): Хост базы данных для проверки

    Returns:
        str: Возвращается исходная строка, если валидация прошла успешно

    Raises:
        InvalidDbHostException: Если хост пустой или None

    Examples:
        >>> validate_db_host("localhost")
        'localhost'
        >>> validate_db_host("")
        Traceback (most recent call last):
        ...
        InvalidDbHostException: Некорректный хост для подключения к БД
    """
    return _validate_is_not_empty_str(host, exc.InvalidDbHostException)


def validate_db_username(username: str) -> str:
    """
    Валидирует имя пользователя базы данных.

    Проверяет, что имя пользователя базы данных не является пустой строкой.
    Используется как валидатор в классе DatabaseConfig.

    Args:
        username (str): Имя пользователя базы данных для проверки

    Returns:
        str: Возвращается исходная строка, если валидация прошла успешно

    Raises:
        InvalidDbUsernameException: Если имя пользователя пустое или None

    Examples:
        >>> validate_db_username("myuser")
        'myuser'
        >>> validate_db_username("")
        Traceback (most recent call last):
        ...
        InvalidDbUsernameException: Некорректное имя пользователя для подключения к БД
    """
    return _validate_is_not_empty_str(username, exc.InvalidDbUsernameException)


def validate_db_password(password: str) -> str:
    """
    Валидирует пароль базы данных.

    Проверяет, что пароль базы данных не является пустой строкой.
    Используется как валидатор в классе DatabaseConfig.

    Args:
        password (str): Пароль базы данных для проверки

    Returns:
        str: Возвращается исходная строка, если валидация прошла успешно

    Raises:
        InvalidDbPasswordException: Если пароль пустой или None

    Examples:
        >>> validate_db_password("mypass")
        'mypass'
        >>> validate_db_password("")
        Traceback (most recent call last):
        ...
        InvalidDbPasswordException: Некорректный пароль для подключения к БД
    """
    return _validate_is_not_empty_str(password, exc.InvalidDbPasswordException)


def validate_db_name(name: str) -> str:
    """
    Валидирует название базы данных.

    Проверяет, что название базы данных не является пустой строкой.
    Используется как валидатор в классе DatabaseConfig.

    Args:
        name (str): Название базы данных для проверки

    Returns:
        str: Возвращается исходная строка, если валидация прошла успешно

    Raises:
        InvalidDbNameException: Если название базы данных пустое или None

    Examples:
        >>> validate_db_name("mydatabase")
        'mydatabase'
        >>> validate_db_name("")
        Traceback (most recent call last):
        ...
        InvalidDbNameException: Некорректное имя БД
    """
    return _validate_is_not_empty_str(name, exc.InvalidDbNameException)


def validate_db_port(port: int) -> int:
    """
    Валидирует порт базы данных.

    Проверяет, что порт базы данных находится в допустимом диапазоне.
    Допустимый диапазон: от MIN_PORT_NUMBER до MAX_PORT_NUMBER (1-65535).
    Используется как валидатор в классе DatabaseConfig.

    Args:
        port (int): Порт базы данных для проверки

    Returns:
        int: Возвращается исходное значение, если валидация прошла успешно

    Raises:
        ValueError: Если порт выходит за пределы допустимого диапазона

    Examples:
        >>> validate_db_port(5432)
        5432
        >>> validate_db_port(65536)
        Traceback (most recent call last):
        ...
        ValueError: Порт вне допустимого диапазона
        >>> validate_db_port(0)
        Traceback (most recent call last):
        ...
        ValueError: Порт вне допустимого диапазона
    """
    try:
        valid_port: int = validate_is_int(port)
    except ValueIsNotIntException as val_exc:
        raise exc.InvalidDbPortException() from val_exc

    if valid_port < MIN_PORT_NUMBER or valid_port > MAX_PORT_NUMBER:
        raise exc.InvalidDbPortException()

    return valid_port


def _validate_is_not_empty_str(value: str, exception: Type[BaseAppException]) -> str:
    """
    Внутренний валидатор для проверки непустых строк.

    Универсальная функция для проверки, что строка не пустая и не None.
    Используется как база для других валидаторов (validate_db_host, validate_db_username и др.).

    Args:
        value (str): Строка для проверки
        exception (Type[BaseAppException]): Тип исключения, которое будет
            возбуждено при неудачной валидации

    Returns:
        str: Возвращается исходная строка, если валидация прошла успешно

    Raises:
        exception: Указанное исключение, если строка пустая или None

    Examples:
        >>> from dh_bl_core.database.exceptions import InvalidDbHostException
        >>> _validate_is_not_empty_str("test", InvalidDbHostException)
        'test'
        >>> _validate_is_not_empty_str("", InvalidDbHostException)
        Traceback (most recent call last):
        ...
        InvalidDbHostException: Некорректный хост для подключения к БД
    """
    try:
        return validate_is_not_empty_str(value)
    except (ValueIsEmptyStrException, ValueIsNotStrException) as val_exc:
        raise exception() from val_exc
