"""Модуль для проверки строк."""

from typing import Any

from .exceptions import ValueIsEmptyStrException, ValueIsNotStrException


def validate_is_str(value: Any) -> str:
    """
    Валидирует, что значение является строкой.

    Проверяет, что переданное значение имеет тип str. Если значение не является
    строкой, возбуждается исключение ValueIsNotStrException.

    Используется как базовый валидатор для других функций, которые работают
    со строковыми данными.

    Args:
        value (Any): Значение любого типа для проверки

    Returns:
        str: Переданное значение, если оно является строкой

    Raises:
        ValueIsNotStrException: Если значение не является экземпляром str

    Examples:
        >>> validate_is_str("hello")
        'hello'
        >>> validate_is_str(123)
        Traceback (most recent call last):
        ...
        ValueIsNotStrException: Переданное значение не является строкой
        >>> validate_is_str(None)
        Traceback (most recent call last):
        ...
        ValueIsNotStrException: Переданное значение не является строкой
    """
    if not isinstance(value, str):
        raise ValueIsNotStrException()

    return value


def validate_is_not_empty_str(value: Any) -> str:
    """
    Валидирует, что значение является непустой строкой.

    Проверяет, что переданное значение является строкой и не пустой (после
    удаления пробельных символов). Использует validate_is_str для проверки
    типа, затем проверяет содержимое строки.

    Args:
        value (Any): Значение любого типа для проверки

    Returns:
        str: Переданная строка с удаленными пробелами по краям,
            если валидация прошла успешно

    Raises:
        ValueIsNotStrException: Если значение не является строкой
        ValueIsEmptyStrException: Если строка пустая или содержит только пробелы

    Examples:
        >>> validate_is_not_empty_str("hello")
        'hello'
        >>> validate_is_not_empty_str("  world  ")
        'world'
        >>> validate_is_not_empty_str("")
        Traceback (most recent call last):
        ...
        ValueIsEmptyStrException: Переданная строка не может быть пустой
        >>> validate_is_not_empty_str("   ")
        Traceback (most recent call last):
        ...
        ValueIsEmptyStrException: Переданная строка не может быть пустой
        >>> validate_is_not_empty_str(123)
        Traceback (most recent call last):
        ...
        ValueIsNotStrException: Переданное значение не является строкой
    """
    valid_value: str = validate_is_str(value)

    if not valid_value or not (valid_value := valid_value.strip()):
        raise ValueIsEmptyStrException()

    return valid_value
