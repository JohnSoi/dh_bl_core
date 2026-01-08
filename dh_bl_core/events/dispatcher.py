"""Диспетчер событий"""

from typing import Any

from .types import EventHandler, EventHandlerType, ListenerType


class EventDispatcher:
    """
    Синглтон-класс для управления событиями в приложении.

    Реализует паттерн "Наблюдатель" (Observer) и позволяет подписываться
    на события и генерировать их. Поддерживает одноразовые и многоразовые обработчики.
    Используется для декомпозиции логики и уменьшения связности между компонентами.

    Attributes:
        _instance (EventDispatcher | None): Статический атрибут для хранения единственного экземпляра класса.
        _listeners (ListenerType): Словарь для хранения обработчиков событий, где ключ - имя события,
            значение - список слушателей.

    Examples:
        >>> # Пример 1: Подписка на событие и его генерация
        >>> async def user_created_handler(data):
        ...     print(f"Создан пользователь: {data['username']}")
        ...
        >>> # Пример 2: Использование одноразового обработчика
        >>> async def welcome_email_handler(data):
        ...     print(f"Отправка приветственного письма для: {data['email']}")
        ...
        >>> async def main():
        ...     event_dispatcher.on("user_created", user_created_handler)
        ...     await event_dispatcher.emit("user_created", {"username": "john_doe"})
        ...     #Создан пользователь: john_doe
        ...
        ...     event_dispatcher.on("user_created", welcome_email_handler, once=True)
        ...     await event_dispatcher.emit("user_created", {"email": "user@example.com"})
        ...     # Отправка приветственного письма для: user@example.com
        ...     await event_dispatcher.emit("user_created", {"email": "another@example.com"})
        ...     # Второй вызов не выполнит обработчик, так как он был одноразовым
    """

    _instance = None

    def __new__(cls):
        """
        Создает или возвращает единственный экземпляр класса (синглтон).

        Метод гарантирует, что в приложении будет существовать только один
        экземпляр EventDispatcher, что необходимо для централизованного
        управления событиями. При первом вызове создает новый экземпляр и
        инициализирует хранилище для слушателей событий.

        Args:
            cls: Класс EventDispatcher.

        Returns:
            EventDispatcher: Единственный экземпляр класса.

        Note:
            Этот метод переопределяет стандартное поведение создания объектов
            и обеспечивает паттерн Синглтон. Должен вызываться интерпретатором Python
            автоматически при создании экземпляра класса.
        """
        if cls._instance:
            return cls._instance

        cls._instance = super(EventDispatcher, cls).__new__(cls)
        cls._instance._listeners = {}
        return cls._instance

    def __init__(self):
        """
        Инициализирует экземпляр диспетчера событий.

        Метод инициализирует хранилище для слушателей событий. В случае синглтона
        этот метод может вызываться несколько раз, но фактически инициализация
        происходит только при первом создании экземпляра.

        """
        self._listeners: ListenerType = {}

    async def emit(self, event_name: str, data: dict | None = None) -> list[Any]:
        """
        Генерирует событие и вызывает все зарегистрированные обработчики.

        Метод проходит по всем слушателям указанного события и выполняет их обработчики.
        Для одноразовых обработчиков (с once=True) производится их удаление после выполнения.
        Возвращает список результатов выполнения всех обработчиков.

        Args:
            event_name (str): Имя события для генерации.
            data (dict | None): Данные, передаваемые обработчикам событий.

        Returns:
            list[Any]: Список результатов выполнения всех обработчиков события.

        Examples:
            >>> async def main():
            ...     # Пример 1: Генерация события с данными
            ...     results = await event_dispatcher.emit("user_login", {"user_id": 123, "ip": "192.168.1.1"})
            ...     print(f"Выполнено {len(results)} обработчиков")
            ...
            ...     # Пример 2: Генерация события без данных
            ...     results = await event_dispatcher.emit("system_start")
            ...     print("Система запущена")
            ...
            ...     # Пример 3: Обработка результатов обработчиков
            ...     results = await event_dispatcher.emit("data_processed", {"count": 100})
            ...     successful = sum(1 for result in results if result is True)
            ...     print(f"Успешно обработано: {successful} из {len(results)}")
        """
        events_results: list[Any] = []

        if event_name not in self._listeners:
            return events_results

        for listener in self._listeners[event_name]:
            handler: EventHandlerType = listener.handler
            is_once: bool = listener.once

            result: Any = await handler(data)
            events_results.append(result)

            if is_once:
                self._listeners[event_name].remove(listener)

        return events_results

    def on(self, event_name: str, handler: EventHandlerType, once: bool = False) -> None:
        """
        Регистрирует обработчик для указанного события.

        Метод добавляет обработчик в список слушателей для указанного события.
        Поддерживает как одноразовые (once=True), так и многоразовые (once=False) обработчики.
        Если список обработчиков для события не существует, он создается.

        Args:
            event_name (str): Имя события, на которое необходимо подписаться.
            handler (EventHandlerType): Асинхронная функция-обработчик события.
            once (bool): Флаг, указывающий, является ли обработчик одноразовым.
                         Если True, обработчик будет автоматически удален после первого вызова.

        Examples:
            >>> # Пример 1: Регистрация многоразового обработчика
            >>> async def log_event(data):
            ...     print(f"[LOG] Событие: {event_name}, Данные: {data}")
            ...
            >>> event_dispatcher.on("user_action", log_event)

            >>> # Пример 2: Регистрация одноразового обработчика
            >>> async def send_welcome_email(data):
            ...     print(f"Отправка приветственного письма для: {data['email']}")
            ...
            >>> event_dispatcher.on("user_registered", send_welcome_email, once=True)

            >>> # Пример 3: Подписка на несколько событий с разными обработчиками
            >>> event_dispatcher.on("order_created", lambda data: print(data))
            >>> event_dispatcher.on("order_created", lambda data: print(data))
            >>> event_dispatcher.on("order_cancelled", lambda data: print(data))
        """
        if event_name not in self._listeners:
            self._listeners[event_name] = []

        self._listeners[event_name].append(EventHandler(handler, once))


event_dispatcher: EventDispatcher = EventDispatcher()
