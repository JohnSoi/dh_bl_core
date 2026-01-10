"""Исключения при работе с сервисом."""

from dh_bl_core.exceptions import InternalServerErrorException


class EmptyRepositoryNotAllowedException(InternalServerErrorException):
    """
    Исключение, возникающее при попытке использовать сервис с пустым репозиторием.

    Это исключение является подклассом InternalServerErrorException и выбрасывается,
    когда происходит обращение к серсвису с пустым репозиторием.

    Attributes:
        _DETAILS (str): Описание ошибки, которое будет включено в ответ.

    Examples:
        >>> # Пример 1: Попытка использовать сервис с пустым репозиторием
        >>> from dh_bl_core.service import BaseService
        >>>
        >>> class MyService(BaseService):
        ...     ...
        ...
        >>> service = MyService()
        Получаем исключение EmptyRepositoryNotAllowedException


    """

    _DETAILS = "Репозиторий не может быть пустым."
