"""Типизация для работы с сервисами."""
from typing import TypeVar

from dh_bl_core.database import BaseRepository as BaseRepositoryClass

# Типизация для репозитория
BaseRepository: TypeVar = TypeVar("BaseRepository", bound=BaseRepositoryClass)
