"""Модуль валидаторов для конфигураций."""

from datetime import datetime
from re import match

from . import exceptions as exc
from .consts import (
    MAX_VERSION_MONTH,
    MIN_VERSION_MONTH,
    VERSION_MIN_YEAR,
    VERSION_REG_EXP,
)


def validate_app_version(version: str) -> str:
    """
    Валидирует формат версии в формате YEAR.MONTH.PATCH.

    Проверяет, что версия соответствует формату YYYY.MM.PATCH, где:
    - YYYY - четырехзначный год (например, 2025, 2026)
    - MM - номер месяца от 01 до 12
    - PATCH - номер патча (целое число)

    Args:
        version (str): Строка с версией для проверки

    Returns:
        str: Возвращается исходная строка, если валидация прошла успешно

    Raises:
        InvalidVersionFormatException: Если формат версии некорректен
            (не соответствует шаблону YEAR.MONTH.PATCH)
        InvalidVersionYearException: Если год в версии выходит за допустимый диапазон
            (меньше VERSION_MIN_YEAR или больше текущего года + 1)
        InvalidVersionMonthException: Если месяц в версии выходит за допустимый диапазон
            (меньше MIN_VERSION_MONTH или больше MAX_VERSION_MONTH)


    Examples:
        >>> validate_app_version("2025.12.1")
        '2025.12.1'
        >>> validate_app_version("2026.01.5")
        '2026.01.5'
        >>> validate_app_version("23.12.1")
        Traceback (most recent call last):
        ...
        ValueError: Версия должна быть в формате YEAR.MONTH.PATCH (например, 2023.12.1)
    """
    print(version)
    if not match(VERSION_REG_EXP, version):
        raise exc.InvalidVersionFormatException()

    year, month, _ = map(int, version.split("."))
    current_year: int = datetime.now().year

    if year < VERSION_MIN_YEAR or year > current_year + 1:
        raise exc.InvalidVersionYearException(current_year)

    if month < MIN_VERSION_MONTH or month > MAX_VERSION_MONTH:
        raise exc.InvalidVersionMonthException()

    return version
