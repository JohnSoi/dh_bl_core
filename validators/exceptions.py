"""Модуль исключений при базовых валидаторов"""
from exceptions import UnprocessableEntityException


class ValueIsNotStrException(UnprocessableEntityException):
    """
    Исключение для ситуации, когда ожидается строка, но передано значение другого типа.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда функция или метод ожидает строковый параметр,
    но получает значение другого типа (число, None, объект и т.д.).

    Используется в валидаторах, которые работают со строками.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise ValueIsNotStrException()
        Traceback (most recent call last):
        ...
        ValueIsNotStrException: Переданное значение не является строкой
        
        >>> def validate_string(value):
        ...     if not isinstance(value, str):
        ...         raise ValueIsNotStrException()
        >>> validate_string(123)
        Traceback (most recent call last):
        ...
        ValueIsNotStrException: Переданное значение не является строкой
    """
    _DETAILS: str = "Переданное значение не является строкой"


class ValueIsEmptyStrException(UnprocessableEntityException):
    """
    Исключение для ситуации, когда передана пустая строка, но ожидается непустая.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда строковый параметр является пустой строкой или содержит
    только пробельные символы, но по логике приложения должен быть непустым.
    Используется в валидаторах, которые проверяют обязательные строковые поля.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise ValueIsEmptyStrException()
        Traceback (most recent call last):
        ...
        ValueIsEmptyStrException: Переданная строка не может быть пустой
        
        >>> def validate_non_empty_string(value: str):
        ...     if not value or not value.strip():
        ...         raise ValueIsEmptyStrException()
        >>> validate_non_empty_string("")
        Traceback (most recent call last):
        ...
        ValueIsEmptyStrException: Переданная строка не может быть пустой
    """
    _DETAILS: str = "Переданная строка не может быть пустой"


class ValueIsNotIntException(UnprocessableEntityException):
    """
    Исключение для ситуации, когда ожидается целое число, но передано значение другого типа.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда функция или метод ожидает целочисленный параметр,
    но получает значение другого типа (строка, None, объект и т.д.).
    Используется в валидаторах, которые работают с числовыми данными.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise ValueIsNotIntException()
        Traceback (most recent call last):
        ...
        ValueIsNotIntException: Переданное значение не является числом
        
        >>> def validate_number(value):
        ...     if not isinstance(value, int):
        ...         raise ValueIsNotIntException()
        >>> validate_number("123")
        Traceback (most recent call last):
        ...
        ValueIsNotIntException: Переданное значение не является числом
    """
    _DETAILS: str = "Переданное значение не является числом"