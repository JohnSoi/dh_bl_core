"""Модуль исключений при проверке параметров конфигурации приложения"""
from exceptions import InternalServerErrorException
from .consts import VERSION_MIN_YEAR, MIN_VERSION_MONTH, MAX_VERSION_MONTH


class InvalidVersionFormatException(InternalServerErrorException):
    """
    Исключение для некорректного формата версии приложения.

    Наследуется от InternalServerErrorException и представляет ошибку 500.
    Возникает, когда строка версии не соответствует ожидаемому формату YEAR.MONTH.PATCH.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию, описывающее
            требуемый формат версии.
        _STATUS_CODE (int): HTTP-код ответа (500).

    Examples:
        >>> raise InvalidVersionFormatException()
        Traceback (most recent call last):
        ...
        InvalidVersionFormatException: Версия должна быть в формате YEAR.MONTH.PATCH (например, 2025.12.1)
    """
    _DETAILS = "Версия должна быть в формате YEAR.MONTH.PATCH (например, 2025.12.1)"


class InvalidVersionYearException(InternalServerErrorException):
    """
    Исключение для недопустимого года в версии приложения.

    Наследуется от InternalServerErrorException и представляет ошибку 500.
    Возникает, когда год в версии выходит за допустимые пределы.
    Допустимый диапазон: от VERSION_MIN_YEAR до текущего года + 1.

    Attributes:
        _STATUS_CODE (int): HTTP-код ответа (500).

    Args:
        current_year (int): Текущий год, используемый для определения
            верхней границы допустимого диапазона.

    Examples:
        >>> raise InvalidVersionYearException(2025)
        Traceback (most recent call last):
        ...
        InvalidVersionYearException: Год в версии должен быть в диапазоне от 2025 до 2026
    """
    def __init__(self, current_year: int) -> None:
        super().__init__(f"Год в версии должен быть в диапазоне от {VERSION_MIN_YEAR} до {current_year + 1}")


class InvalidVersionMonthException(InternalServerErrorException):
    """
    Исключение для недопустимого месяца в версии приложения.

    Наследуется от InternalServerErrorException и представляет ошибку 500.
    Возникает, когда месяц в версии выходит за допустимые пределы (от 1 до 12).
    Значения берутся из констант MIN_VERSION_MONTH и MAX_VERSION_MONTH.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию, содержащее
            допустимый диапазон месяцев.
        _STATUS_CODE (int): HTTP-код ответа (500).

    Examples:
        >>> raise InvalidVersionMonthException()
        Traceback (most recent call last):
        ...
        InvalidVersionMonthException: Месяц в версии должен быть в диапазоне от 1 до 12
    """
    _DETAILS = f"Месяц в версии должен быть в диапазоне от {MIN_VERSION_MONTH} до {MAX_VERSION_MONTH}"
