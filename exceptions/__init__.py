"""Пакет базовых исключений приложений"""

from .common import (
    BadRequestException,
    BaseAppException,
    ConflictException,
    ForbiddenException,
    InternalServerErrorException,
    MethodNotAllowedException,
    NotFoundException,
    NotImplementedException,
    ServiceUnavailableException,
    TooManyRequestsException,
    UnauthorizedException,
    UnprocessableEntityException,
)
