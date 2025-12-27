"""Модуль для проверки чисел."""

from typing import Any

from .exceptions import ValueIsNotIntException


def validate_is_int(value: Any) -> int:
    """Валидирует, что значение является целым числом.

    Проверяет, что переданное значение имеет тип int. Если значение не является
    целым числом, возбуждается исключение ValueIsNotIntException.
    Используется как базовый валидатор для других функций, которые работают
    с числовыми данными.

    Args:
        value (Any): Значение любого типа для проверки

    Returns:
        int: Переданное значение, если оно является целым числом

    Raises:
        ValueIsNotIntException: Если значение не является экземпляром int

    Examples:
        >>> validate_is_int(123)
        123
        >>> validate_is_int("123")
        Traceback (most recent call last):
        ...
        ValueIsNotIntException: Переданное значение не является числом
        >>> validate_is_int(12.5)
        Traceback (most recent call last):
        ...
        ValueIsNotIntException: Переданное значение не является числом
        >>> validate_is_int(None)
        Traceback (most recent call last):
        ...
        ValueIsNotIntException: Переданное значение не является числом
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueIsNotIntException()

    return value
