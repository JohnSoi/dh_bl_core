# pylint: disable=too-few-public-methods
"""Модуль для логирования запросов и ответов."""
from typing import Awaitable, Callable

from fastapi import Request, Response
from x_request_id_middleware.common import get_x_request_id

from dh_bl_core.logging import LogManager


class LogRequestResponseMiddleware:
    """
    Middleware для логирования входящих запросов и исходящих ответов.

    Этот класс реализует middleware для FastAPI, который автоматически логирует
    информацию о входящих HTTP-запросах и исходящих ответах. Поддерживает логирование
    с идентификатором запроса (X-Request-ID) для трассировки.

    Attributes:
        _LOGGER (Logger): Экземпляр логгера для записи информации о запросах и ответах.

    Examples:
        >>> from fastapi import FastAPI
        >>> from dh_bl_core.api.middlewares.log_req_resp import LogRequestResponseMiddleware
        >>>
        >>> app = FastAPI()
        >>> # Регистрация middleware
        >>> app.add_middleware(LogRequestResponseMiddleware)
        >>>
        >>> @app.get("/")
        ... async def root():
        ...     return {"message": "Hello World"}
        >>>
        >>> # При вызове эндпоинта будут автоматически залогированы запрос и ответ
        >>> # INFO:     [req] Запрос методом GET на /
        >>> # INFO:     [req] Ответ 200 на /
    """

    _LOGGER = LogManager("req").logger

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """
        Обрабатывает входящий запрос и исходящий ответ, выполняя их логирование.

        Метод вызывается автоматически фреймворком FastAPI для каждого входящего запроса.
        Логирует информацию о запросе до его обработки и информацию об ответе после
        обработки. Включает в лог дополнительные данные: параметры запроса, заголовки
        и тело ответа.

        Args:
            request (Request): Объект входящего HTTP-запроса от FastAPI.
            call_next (Callable[[Request], Awaitable[Response]]): Функция для вызова
                следующего middleware или обработчика маршрута в цепочке.

        Returns:
            Response: Объект HTTP-ответа, возвращаемый после обработки запроса.

        Note:
            Метод автоматически проверяет наличие заголовка X-Request-ID
            и включает его в лог, если он присутствует. Это позволяет связать
            логи запроса и ответа в распределенной системе.

        Examples:
            >>> # Внутреннее использование в FastAPI
            >>> # Метод вызывается автоматически при поступлении запроса
            >>> # Пример лога без X-Request-ID:
            >>> # INFO:     [req] Запрос методом GET на /api/users
            >>> # INFO:     [req] Ответ 200 на /api/users
            >>>
            >>> # Пример лога с X-Request-ID:
            >>> # INFO:     [req] Запрос 123e4567-e89b-12d3-a456-426614174000 методом POST на /api/login
            >>> # INFO:     [req] Ответ 201 на /api/login
            >>>
            >>> # Логирование включает дополнительные данные:
            >>> # - Параметры запроса (все атрибуты объекта Request)
            >>> # - Заголовки запроса
            >>> # - Тело ответа (все атрибуты объекта Response)
        """
        url: str = request.url.path
        method: str = request.method
        x_request_id: str | None = get_x_request_id()

        if x_request_id:
            self._LOGGER.info(
                f"Запрос {x_request_id} методом {method} на {url}",
                extra={"params": request.__dict__, "headers": request.headers},
            )
        else:
            self._LOGGER.info(
                f"Запрос методом {method} на {url}", extra={"params": request.__dict__, "headers": request.headers}
            )

        response: Response = await call_next(request)
        status_code: int = response.status_code

        self._LOGGER.info(f"Ответ {status_code} на {url}", extra={"response": response.__dict__})

        return response
