"""Пакет базовых исключений приложений"""

from .common import BaseAppException, ConflictException, ForbiddenException, NotFoundException, UnauthorizedException, \
    NotImplementedException, MethodNotAllowedException, UnprocessableEntityException, BadRequestException, \
    TooManyRequestsException, ServiceUnavailableException, InternalServerErrorException
