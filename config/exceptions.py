"""Модуль исключений при проверке параметров конфигурации приложения"""
from exceptions import UnprocessableEntityException
from .consts import VERSION_MIN_YEAR, MIN_VERSION_MONTH, MAX_VERSION_MONTH, MIN_PORT_NUMBER, MAX_PORT_NUMBER


class InvalidVersionFormatException(UnprocessableEntityException):
    """
    Исключение для некорректного формата версии приложения.

    Наследуется от UnprocessableEntityException и представляет ошибку 500.
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


class InvalidVersionYearException(UnprocessableEntityException):
    """
    Исключение для недопустимого года в версии приложения.

    Наследуется от UnprocessableEntityException и представляет ошибку 500.
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


class InvalidVersionMonthException(UnprocessableEntityException):
    """
    Исключение для недопустимого месяца в версии приложения.

    Наследуется от UnprocessableEntityException и представляет ошибку 500.
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


class InvalidDbHostException(UnprocessableEntityException):
    """
    Исключение для некорректного хоста подключения к базе данных.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда хост базы данных не проходит валидацию (пустой или некорректный).

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise InvalidDbHostException()
        Traceback (most recent call last):
        ...
        InvalidDbHostException: Некорректный хост для подключения к БД
    """
    _DETAILS = "Некорректный хост для подключения к БД"


class InvalidDbUsernameException(UnprocessableEntityException):
    """
    Исключение для некорректного имени пользователя базы данных.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда имя пользователя базы данных не проходит валидацию
    (пустое или некорректное).

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise InvalidDbUsernameException()
        Traceback (most recent call last):
        ...
        InvalidDbUsernameException: Некорректное имя пользователя для подключения к БД
    """
    _DETAILS = "Некорректное имя пользователя для подключения к БД"


class InvalidDbPasswordException(UnprocessableEntityException):
    """
    Исключение для некорректного пароля базы данных.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда пароль базы данных не проходит валидацию (пустой).

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise InvalidDbPasswordException()
        Traceback (most recent call last):
        ...
        InvalidDbPasswordException: Некорректный пароль для подключения к БД
    """
    _DETAILS = "Некорректный пароль для подключения к БД"


class InvalidDbNameException(UnprocessableEntityException):
    """
    Исключение для некорректного названия базы данных.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда название базы данных не проходит валидацию (пустое или некорректное).

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise InvalidDbNameException()
        Traceback (most recent call last):
        ...
        InvalidDbNameException: Некорректное имя БД
    """
    _DETAILS = "Некорректное имя БД"


class InvalidDbPortException(UnprocessableEntityException):
    """
    Исключение для некорректного порта подключения к базе данных.

    Наследуется от UnprocessableEntityException и представляет ошибку 422.
    Возникает, когда порт базы данных выходит за допустимый диапазон.
    Допустимый диапазон: от MIN_PORT_NUMBER до MAX_PORT_NUMBER.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию, содержащее
            допустимый диапазон портов.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise InvalidDbPortException()
        Traceback (most recent call last):
        ...
        InvalidDbPortException: Некорректный порт для подключения к БД. Допустимый диапазон: от 1 до 65535
    """
    _DETAILS = f"Некорректный порт для подключения к БД. Допустимый диапазон: от {MIN_PORT_NUMBER} до {MAX_PORT_NUMBER}"
