"""Модуль исключений приложения."""

from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    """
    Базовый класс для всех пользовательских исключений приложения.

    Этот класс служит основой для всех специфических исключений в приложении.
    Наследуется от FastAPI HTTPException и добавляет дополнительные проверки
    при создании экземпляров исключений. Обеспечивает обязательное наличие
    либо детального описания ошибки, либо HTTP-кода.

    Attributes:
        _DETAILS (str | None): Статическое сообщение об ошибке по умолчанию.
            Должно быть переопределено в дочерних классах.
        _STATUS_CODE (int | None): Статический HTTP-код ответа по умолчанию.
            Должен быть переопределен в дочерних классах.

    Args:
        details (str | None): Детальное сообщение об ошибке. Если не указано,
            будет использовано значение _DETAILS из класса.
        status_code (int | None): HTTP-код ответа. Если не указан,
            будет использовано значение _STATUS_CODE из класса.

    Raises:
        ValueError: Если не передано ни details, ни _DETAILS, или не передан
            ни status_code, ни _STATUS_CODE.

    Examples:
        >>> class CustomException(BaseAppException):
        ...     _DETAILS = "Кастомная ошибка"
        ...     _STATUS_CODE = 400
        >>>
        >>> # Создание исключения с переопределением сообщения
        >>> raise CustomException(details="Детали ошибки")
        Traceback (most recent call last):
        ...
        CustomException: Детали ошибки

        >>> # Создание исключения с использованием сообщения по умолчанию
        >>> raise CustomException()
        Traceback (most recent call last):
        ...
        CustomException: Кастомная ошибка
    """
    _DETAILS: str | None = None
    _STATUS_CODE: int | None = None

    def __init__(self, details: str | None = None, status_code: int | None = None):
        """
        Инициализирует экземпляр исключения.

        Проверяет наличие необходимых параметров (сообщение и HTTP-код) и создает
        исключение с соответствующими параметрами. Позволяет переопределять
        сообщение и код ошибки при создании экземпляра.

        Args:
            details (str | None): Детальное сообщение об ошибке. Если не указано,
                будет использовано значение _DETAILS из класса.
            status_code (int | None): HTTP-код ответа. Если не указан,
                будет использовано значение _STATUS_CODE из класса.

        Raises:
            ValueError: Если не передано ни details, ни _DETAILS, или не передан
                ни status_code, ни _STATUS_CODE.

        Examples:
            >>> exc = BaseAppException(details="Ошибка", status_code=400)
            >>> exc.detail
            'Ошибка'
            >>> exc.status_code
            400
        """
        if not any((details, self._DETAILS)):
            raise ValueError("Нельзя создать исключение без пояснительного сообщения.")

        if not any((status_code, self._STATUS_CODE)):
            raise ValueError("Нельзя создать исключение без HTTP-кода.")

        super().__init__(detail=details or self._DETAILS, status_code=status_code or self._STATUS_CODE)


class NotFoundException(BaseAppException):
    """
    Исключение для ситуации, когда запрашиваемый ресурс не найден.

    Наследуется от BaseAppException и представляет HTTP 404 Not Found ошибку.
    Используется, когда сервер не может найти запрашиваемый ресурс.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (404).

    Examples:
        >>> raise NotFoundException()
        Traceback (most recent call last):
        ...
        NotFoundException: Не удалось найти ресурс по переданным параметрам.

        >>> raise NotFoundException(details="Пользователь не найден")
        Traceback (most recent call last):
        ...
        NotFoundException: Пользователь не найден
    """
    _DETAILS: str = "Не удалось найти ресурс по переданным параметрам."
    _STATUS_CODE: int = status.HTTP_404_NOT_FOUND


class BadRequestException(BaseAppException):
    """
    Исключение для ситуации, когда клиент отправил некорректный запрос.

    Наследуется от BaseAppException и представляет HTTP 400 Bad Request ошибку.
    Используется, когда сервер не может обработать запрос из-за неверного синтаксиса.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (400).

    Examples:
        >>> raise BadRequestException()
        Traceback (most recent call last):
        ...
        BadRequestException: В запросе допущена ошибка.

        >>> raise BadRequestException(details="Некорректный email")
        Traceback (most recent call last):
        ...
        BadRequestException: Некорректный email
    """
    _DETAILS: str = "В запросе допущена ошибка."
    _STATUS_CODE: int = status.HTTP_400_BAD_REQUEST


class UnauthorizedException(BaseAppException):
    """
    Исключение для ситуации, когда требуется аутентификация.

    Наследуется от BaseAppException и представляет HTTP 401 Unauthorized ошибку.
    Используется, когда запрос требует аутентификации, но она не была предоставлена.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (401).

    Examples:
        >>> raise UnauthorizedException()
        Traceback (most recent call last):
        ...
        UnauthorizedException: Для доступа к ресурсу требуется аутентификация.

        >>> raise UnauthorizedException(details="Токен истек")
        Traceback (most recent call last):
        ...
        UnauthorizedException: Токен истек
    """
    _DETAILS: str = "Для доступа к ресурсу требуется аутентификация."
    _STATUS_CODE: int = status.HTTP_401_UNAUTHORIZED


class ForbiddenException(BaseAppException):
    """
    Исключение для ситуации, когда доступ к ресурсу запрещен.

    Наследуется от BaseAppException и представляет HTTP 403 Forbidden ошибку.
    Используется, когда сервер понимает запрос, но отказывается его авторизовать.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (403).

    Examples:
        >>> raise ForbiddenException()
        Traceback (most recent call last):
        ...
        ForbiddenException: У вас недостаточно прав для доступа к ресурсу.

        >>> raise ForbiddenException(details="Недостаточно прав администратора")
        Traceback (most recent call last):
        ...
        ForbiddenException: Недостаточно прав администратора
    """
    _DETAILS: str = "У вас недостаточно прав для доступа к ресурсу."
    _STATUS_CODE: int = status.HTTP_403_FORBIDDEN


class ConflictException(BaseAppException):
    """
    Исключение для ситуации конфликта при выполнении операции.

    Наследуется от BaseAppException и представляет HTTP 409 Conflict ошибку.
    Используется, когда запрос не может быть выполнен из-за конфликта
    в текущем состоянии ресурса.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (409).

    Examples:
        >>> raise ConflictException()
        Traceback (most recent call last):
        ...
        ConflictException: Ресурс с такими параметрами уже существует.

        >>> raise ConflictException(details="Пользователь с таким email уже существует")
        Traceback (most recent call last):
        ...
        ConflictException: Пользователь с таким email уже существует
    """
    _DETAILS: str = "Ресурс с такими параметрами уже существует."
    _STATUS_CODE: int = status.HTTP_409_CONFLICT


class InternalServerErrorException(BaseAppException):
    """
    Исключение для внутренних ошибок сервера.

    Наследуется от BaseAppException и представляет HTTP 500 Internal Server Error.
    Используется, когда на сервере произошла непредвиденная ошибка.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (500).

    Examples:
        >>> raise InternalServerErrorException()
        Traceback (most recent call last):
        ...
        InternalServerErrorException: Внутренняя ошибка сервера.

        >>> raise InternalServerErrorException(details="Ошибка базы данных")
        Traceback (most recent call last):
        ...
        InternalServerErrorException: Ошибка базы данных
    """
    _DETAILS: str = "Внутренняя ошибка сервера."
    _STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR


class ServiceUnavailableException(BaseAppException):
    """
    Исключение для ситуации, когда сервис временно недоступен.

    Наследуется от BaseAppException и представляет HTTP 503 Service Unavailable.
    Используется, когда сервер временно не может обработать запрос.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (503).

    Examples:
        >>> raise ServiceUnavailableException()
        Traceback (most recent call last):
        ...
        ServiceUnavailableException: Сервис недоступен.

        >>> raise ServiceUnavailableException(details="Техническое обслуживание")
        Traceback (most recent call last):
        ...
        ServiceUnavailableException: Техническое обслуживание
    """
    _DETAILS: str = "Сервис недоступен."
    _STATUS_CODE: int = status.HTTP_503_SERVICE_UNAVAILABLE


class TooManyRequestsException(BaseAppException):
    """
    Исключение для ситуации превышения лимита запросов.

    Наследуется от BaseAppException и представляет HTTP 429 Too Many Requests.
    Используется, когда пользователь отправил слишком много запросов за
    определенный период времени.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (429).

    Examples:
        >>> raise TooManyRequestsException()
        Traceback (most recent call last):
        ...
        TooManyRequestsException: Слишком много запросов. Попробуйте позже.

        >>> raise TooManyRequestsException(details="Лимит запросов исчерпан")
        Traceback (most recent call last):
        ...
        TooManyRequestsException: Лимит запросов исчерпан
    """
    _DETAILS: str = "Слишком много запросов. Попробуйте позже."
    _STATUS_CODE: int = status.HTTP_429_TOO_MANY_REQUESTS


class UnprocessableEntityException(BaseAppException):
    """
    Исключение для ситуации, когда сущность не может быть обработана.

    Наследуется от BaseAppException и представляет HTTP 422 Unprocessable Entity.
    Используется, когда сервер понимает тип содержимого запроса и синтаксис,
    но не может обработать инструкции.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (422).

    Examples:
        >>> raise UnprocessableEntityException()
        Traceback (most recent call last):
        ...
        UnprocessableEntityException: Неверный формат данных.

        >>> raise UnprocessableEntityException(details="Поле email обязательно")
        Traceback (most recent call last):
        ...
        UnprocessableEntityException: Поле email обязательно
    """
    _DETAILS: str = "Неверный формат данных."
    _STATUS_CODE: int = status.HTTP_422_UNPROCESSABLE_CONTENT


class NotImplementedException(BaseAppException):
    """
    Исключение для ситуации, когда запрашиваемый функционал не реализован.

    Наследуется от BaseAppException и представляет HTTP 501 Not Implemented.
    Используется, когда сервер не поддерживает функциональность, необходимую
    для выполнения запроса.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (501).

    Examples:
        >>> raise NotImplementedException()
        Traceback (most recent call last):
        ...
        NotImplementedException: Запрашиваемый Вами ресурс не реализован.

        >>> raise NotImplementedException(details="Метод еще в разработке")
        Traceback (most recent call last):
        ...
        NotImplementedException: Метод еще в разработке
    """
    _DETAILS: str = "Запрашиваемый Вами ресурс не реализован."
    _STATUS_CODE: int = status.HTTP_501_NOT_IMPLEMENTED


class MethodNotAllowedException(BaseAppException):
    """
    Исключение для ситуации, когда метод не разрешен для ресурса.

    Наследуется от BaseAppException и представляет HTTP 405 Method Not Allowed.
    Используется, когда сервер знает о методе, но он не поддерживается
    для данного ресурса.

    Attributes:
        _DETAILS (str): Сообщение об ошибке по умолчанию.
        _STATUS_CODE (int): HTTP-код ответа (405).

    Examples:
        >>> raise MethodNotAllowedException()
        Traceback (most recent call last):
        ...
        MethodNotAllowedException: Данный метод не поддерживается для данного ресурса.

        >>> raise MethodNotAllowedException(details="Метод PUT не поддерживается")
        Traceback (most recent call last):
        ...
        MethodNotAllowedException: Метод PUT не поддерживается
    """
    _DETAILS: str = "Данный метод не поддерживается для данного ресурса."
    _STATUS_CODE: int = status.HTTP_405_METHOD_NOT_ALLOWED
