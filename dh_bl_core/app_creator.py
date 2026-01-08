"""Модуль для создания FastAPI приложения."""

from fastapi import FastAPI
from x_request_id_middleware.fastapi_middleware import FastAPIXRequestIDMiddleware

from dh_bl_core.api.middlewares import LogRequestResponseMiddleware
from dh_bl_core.config import AppConfig, get_app_config
from dh_bl_core.logging import LogManager


class AppCreator:
    """
    Синглтон-класс для создания и настройки экземпляра FastAPI приложения.

    Этот класс реализует паттерн Синглтон и предоставляет централизованный способ
    создания экземпляра FastAPI приложения с предустановленными middleware и
    конфигурацией. Гарантирует, что в приложении будет существовать только один
    экземпляр создателя приложения.

    Attributes:
        _instance (AppCreator | None): Статический атрибут для хранения единственного
            экземпляра класса.
        _LOGGER (Logger): Экземпляр логгера для записи информации о процессе создания приложения.
        _BASE_MIDDLEWARES (list): Список базовых middleware, которые добавляются
            к каждому создаваемому приложению по умолчанию.
        _middlewares (list): Список middleware, которые будут добавлены к приложению.

    Examples:
        >>> # Пример 1: Создание экземпляра AppCreator и приложения
        >>> from dh_bl_core.app_creator import AppCreator
        >>>
        >>> creator = AppCreator()
        >>> app = creator.create_app()
        >>>
        >>> # Пример 2: Добавление кастомного middleware перед созданием приложения
        >>> from fastapi.middleware.cors import CORSMiddleware
        >>> creator = AppCreator()
        >>> creator.add_middleware(CORSMiddleware)
        >>> app = creator.create_app()
        >>>
        >>> # Пример 3: Гарантия единственности экземпляра (синглтон)
        >>> creator1 = AppCreator()
        >>> creator2 = AppCreator()
        >>> creator1 is creator2
        True
    """

    _instance = None
    _LOGGER = LogManager("a_c").logger
    _BASE_MIDDLEWARES = [FastAPIXRequestIDMiddleware, LogRequestResponseMiddleware]

    def __new__(cls):
        """
        Создает или возвращает существующий экземпляр класса (синглтон).

        Метод гарантирует, что в приложении будет существовать только один
        экземпляр AppCreator. При первом вызове создает новый экземпляр и
        инициализирует его middleware. При последующих вызовах возвращает
        уже существующий экземпляр.

        Args:
            cls: Класс AppCreator.

        Returns:
            AppCreator: Единственный экземпляр класса.

        Note:
            Этот метод переопределяет стандартное поведение создания объектов
            и обеспечивает паттерн Синглтон. Должен вызываться интерпретатором Python
            автоматически при создании экземпляра класса.

        Examples:
            >>> # Внутреннее использование при создании экземпляра
            >>> # Метод вызывается автоматически при AppCreator()
            >>> creator1 = AppCreator()  # Создается новый экземпляр
            >>> creator2 = AppCreator()  # Возвращается существующий экземпляр
            >>> creator1 is creator2
            True
            >>>
            >>> # Проверка логирования
            >>> # При первом создании:
            >>> # DEBUG:    [a_c] AppCreator создан
            >>> # При последующих вызовах:
            >>> # DEBUG:    [a_c] AppCreator уже создан
        """
        if cls._instance:
            cls._LOGGER.debug("AppCreator уже создан")
            return cls._instance

        cls._instance = super(AppCreator, cls).__new__(cls)
        cls._instance._middlewares = AppCreator._BASE_MIDDLEWARES.copy()
        cls._LOGGER.debug("AppCreator создан")
        return cls._instance

    def __init__(self) -> None:
        """
        Инициализирует экземпляр AppCreator.

        Метод инициализирует список middleware для текущего экземпляра,
        копируя базовые middleware. В случае синглтона этот метод может
        вызываться несколько раз, но фактическая инициализация происходит
        только при первом создании экземпляра.

        Note:
            Поскольку AppCreator реализует паттерн Синглтон, этот метод
            может быть вызван многократно, но реальная инициализация
            происходит только при первом создании экземпляра в методе __new__.

        Examples:
            >>> # Внутреннее использование при создании экземпляра
            >>> # Метод вызывается автоматически после __new__
            >>> creator = AppCreator()  # __init__ вызывается автоматически
            >>> len(creator._middlewares) > 0
            True
        """
        self._middlewares: list = AppCreator._BASE_MIDDLEWARES.copy()

    def add_middleware(self, middleware) -> None:
        """
        Добавляет middleware в список middleware для приложения.

        Метод позволяет добавить дополнительный middleware к списку middleware,
        которые будут применены к создаваемому приложению. Middleware будут добавлены
        в порядке их регистрации.

        Args:
            middleware: Экземпляр middleware, который должен быть добавлен.
                Может быть любым совместимым middleware для FastAPI.

        Examples:
            >>> from dh_bl_core.app_creator import AppCreator
            >>> from fastapi.middleware.cors import CORSMiddleware
            >>>
            >>> creator = AppCreator()
            >>> # Добавление CORS middleware
            >>> creator.add_middleware(CORSMiddleware)
            >>> # Добавление кастомного middleware
            >>> creator.add_middleware(LogRequestResponseMiddleware)
            >>> # Создание приложения с добавленными middleware
            >>> app = creator.create_app()
            >>>
            >>> # Middleware будут применены в порядке добавления
            >>> # При создании приложения все зарегистрированные middleware
            >>> # будут автоматически добавлены через app.add_middleware()
        """
        self._middlewares.append(middleware)

    def create_app(self) -> FastAPI:
        """
        Создает и настраивает экземпляр FastAPI приложения.

        Метод создает новый экземпляр FastAPI приложения с конфигурацией из AppConfig,
        добавляет все зарегистрированные middleware и возвращает готовое приложение.
        Используется для централизованного создания приложения с едиными настройками.

        Returns:
            FastAPI: Настроенный экземпляр FastAPI приложения с зарегистрированными middleware.

        Note:
            Метод получает конфигурацию приложения через get_app_config() и использует
            ее для установки заголовка и версии приложения. Все middleware, добавленные
            через add_middleware(), применяются к приложению в порядке их регистрации.

        Examples:
            >>> from dh_bl_core.app_creator import AppCreator
            >>>
            >>> # Создание приложения с базовыми middleware
            >>> creator = AppCreator()
            >>> app = creator.create_app()
            >>> app.title
            'Default App Title'
            >>> app.version
            '1.0.0'
            >>>
            >>> # Создание приложения с кастомными middleware
            >>> from fastapi.middleware.cors import CORSMiddleware
            >>> creator = AppCreator()
            >>> creator.add_middleware(CORSMiddleware)
            >>> app = creator.create_app()
            >>> # Приложение будет иметь зарегистрированные middleware
            >>> # включая базовые и добавленные
        """
        app_settings: AppConfig = get_app_config()
        app: FastAPI = FastAPI(title=app_settings.name, version=app_settings.version)

        for middleware in self._middlewares:
            app.add_middleware(middleware)

        return app


# Создание глобального экземпляра AppCreator
app_creator: AppCreator = AppCreator()
