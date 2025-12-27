import re

from .consts import CAMEL_REGEX, SNAKE_REGEX_REPLACE


def camel_to_snake_case(name: str) -> str:
    snake: str = re.sub(CAMEL_REGEX, SNAKE_REGEX_REPLACE, name).replace('__', '_')

    return snake.lower()
