"""Вспомогательные функции для работы со строками."""

import re

from .consts import CAMEL_REGEX, SNAKE_REGEX_REPLACE


def camel_to_snake_case(name: str) -> str:
    """
    Преобразует строку из camelCase в snake_case.

    Функция использует регулярное выражение для определения границ слов
    в camelCase формате и преобразует их в snake_case с помощью замены
    из констант CAMEL_REGEX и SNAKE_REGEX_REPLACE.

    Args:
        name (str): Строка в формате camelCase для преобразования.

    Returns:
        str: Строка в формате snake_case.

    Examples:
        >>> camel_to_snake_case('camelCase')
        'camel_case'
        >>> camel_to_snake_case('getHTTPResponseCode')
        'get_http_response_code'
        >>> camel_to_snake_case('XMLHttpRequest')
        'xml_http_request'
        >>> camel_to_snake_case('number2Word')
        'number2_word'
    """
    snake: str = re.sub(CAMEL_REGEX, SNAKE_REGEX_REPLACE, name).replace("__", "_")

    return snake.lower()
