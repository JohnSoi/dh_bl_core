"""Типизация для работы с событиями."""

from dataclasses import dataclass
from typing import Any, Callable, TypeAlias

EventHandlerType: TypeAlias = Callable[[dict | None], Any]


@dataclass
class EventHandler:
    """
    Тип обработчика события.

    Тип-псевдоним для функций-обработчиков событий. Обработчик события - это асинхронная функция,
    которая принимает словарь с данными (или None) и возвращает значение любого типа.

    Используется для аннотации типов в системе событий, обеспечивая типобезопасность
    и поддержку IDE.

    Examples:
        >>> # Пример 1: Определение обработчика события
        >>> async def user_created_handler(data: dict | None) -> bool:
        ...     '''Обработчик события создания пользователя'''
        ...     if data and data.get("email"):
        ...         print(f"Отправка приветственного письма на {data['email']}")
        ...         return True
        ...     return False
        ...
        >>> # Проверка соответствия типу EventHandlerType
        >>> isinstance(user_created_handler, EventHandlerType)
        True

        >>> # Пример 2: Использование в аннотации параметра
        >>> def subscribe_to_event(event_name: str, handler: EventHandlerType) -> None:
        ...     '''Подписаться на событие с указанным обработчиком'''
        ...     event_dispatcher.on(event_name, handler)
        ...
        >>> subscribe_to_event("user_created", user_created_handler)
    """

    handler: EventHandlerType
    once: bool


# Тип слушателей событий
ListenerType: TypeAlias = dict[str, list[EventHandler]]
