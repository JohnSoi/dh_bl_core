# pylint: disable=too-few-public-methods
"""Модуль для логирования времени выполнения запросов."""
import time
from typing import Awaitable, Callable

from fastapi import Request, Response

from dh_bl_core.logging import LogManager


class RequestTimeMiddleware:
    """
    Middleware для измерения и логирования времени выполнения запросов.

    Этот класс реализует middleware для FastAPI, который измеряет время выполнения
    каждого запроса, добавляет его в заголовок ответа X-Response-Time и логирует
    информацию о времени выполнения. Позволяет отслеживать производительность
    эндпоинтов и выявлять узкие места в приложении.

    Attributes:
        _LOGGER (Logger): Экземпляр логгера для записи информации о времени выполнения.

    Examples:
        >>> from fastapi import FastAPI
        >>> from dh_bl_core.api.middlewares.request_time import RequestTimeMiddleware
        >>>
        >>> app = FastAPI()
        >>> # Регистрация middleware
        >>> app.add_middleware(RequestTimeMiddleware)
        >>>
        >>> @app.get("/")
        ... async def root():
        ...     return {"message": "Hello World"}
        >>>
        >>> # При вызове эндпоинта будет добавлен заголовок и записан лог:
        >>> # X-Response-Time: 12.34ms
        >>> # INFO:     [time] Время выполнения запроса: 12.34ms
        >>>
        >>> # В реальном ответе клиенту будет добавлен заголовок X-Response-Time
        >>> # с указанием времени выполнения в миллисекундах
    """

    _LOGGER = LogManager("time").logger

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """
        Измеряет время выполнения запроса и добавляет его в заголовок ответа.

        Метод вызывается автоматически фреймворком FastAPI для каждого входящего запроса.
        Фиксирует время начала и окончания обработки запроса, вычисляет время выполнения
        в миллисекундах и добавляет его в заголовок X-Response-Time ответа. Также логирует
        время выполнения для последующего анализа производительности.

        Args:
            request (Request): Объект входящего HTTP-запроса от FastAPI.
            call_next (Callable[[Request], Awaitable[Response]]): Функция для вызова
                следующего middleware или обработчика маршрута в цепочке.

        Returns:
            Response: Объект HTTP-ответа с добавленным заголовком X-Response-Time,
                содержащим время выполнения запроса в миллисекундах.

        Note:
            Время измеряется с высокой точностью с использованием time.perf_counter(),
            что обеспечивает наиболее точные результаты. Значение времени округляется
            до двух знаков после запятой для удобства чтения.

        Examples:
            >>> # Внутреннее использование в FastAPI
            >>> # Метод вызывается автоматически при поступлении запроса
            >>> # Пример ответа клиенту:
            >>> # HTTP/1.1 200 OK
            >>> # X-Response-Time: 45.67ms
            >>> # Content-Type: application/json
            >>> #
            >>> # {"message": "Hello World"}
            >>>
            >>> # Пример лога:
            >>> # INFO:     [time] Время выполнения запроса: 45.67ms
            >>>
            >>> # Заголовок X-Response-Time может использоваться клиентом для анализа
            >>> # производительности API и отладки проблем с задержками
        """
        start_time: float = time.perf_counter()
        response: Response = await call_next(request)
        end_time: float = time.perf_counter()
        execution_time_ms: float = (end_time - start_time) * 1000
        response.headers["X-Response-Time"] = f"{execution_time_ms:.2f}ms"

        self._LOGGER.info(f"Время выполнения запроса: {execution_time_ms:.2f}ms")

        return response
