"""
Тесты для валидаторов конфигурации приложения.

Этот модуль содержит тесты для проверки функций валидации параметров конфигурации
приложения, за исключением validate_app_version и _validate_is_not_empty_str.
Тесты проверяют корректность работы валидаторов для различных сценариев.
"""

import pytest

from config.exceptions import (
    InvalidDbHostException,
    InvalidDbNameException,
    InvalidDbPasswordException,
    InvalidDbPortException,
    InvalidDbUsernameException,
)
from config.validators import (
    validate_db_host,
    validate_db_name,
    validate_db_password,
    validate_db_port,
    validate_db_username,
)


class TestDbConfigValidators:
    """Тестовый класс для проверки валидаторов конфигурации БД."""

    def test_validate_db_host_valid(self):
        """Проверяет, что корректный хост проходит валидацию."""
        # Тестирование корректных хостов
        valid_hosts = [
            "localhost",
            "127.0.0.1",
            "192.168.1.1",
            "example.com",
            "db-server.prod",
            "my-db-host",
        ]

        for host in valid_hosts:
            assert validate_db_host(host) == host

    def test_validate_db_host_invalid(self):
        """Проверяет, что некорректные хосты вызывают исключение."""
        # Тестирование некорректных хостов
        invalid_hosts = [
            "",  # Пустая строка
            "   ",  # Только пробелы
            None,  # None (будет вызывать исключение через внутренний валидатор)
        ]

        for host in invalid_hosts:
            with pytest.raises(InvalidDbHostException):
                validate_db_host(host)

    def test_validate_db_username_valid(self):
        """Проверяет, что корректное имя пользователя проходит валидацию."""
        # Тестирование корректных имен пользователей
        valid_usernames = [
            "admin",
            "user123",
            "my_username",
            "db_user_prod",
            "service-account",
        ]

        for username in valid_usernames:
            assert validate_db_username(username) == username

    def test_validate_db_username_invalid(self):
        """Проверяет, что некорректные имена пользователей вызывают исключение."""
        # Тестирование некорректных имен пользователей
        invalid_usernames = [
            "",  # Пустая строка
            "   ",  # Только пробелы
            None,  # None
        ]

        for username in invalid_usernames:
            with pytest.raises(InvalidDbUsernameException):
                validate_db_username(username)

    def test_validate_db_password_valid(self):
        """Проверяет, что корректный пароль проходит валидацию."""
        # Тестирование корректных паролей
        valid_passwords = [
            "password123",
            "secret-pass",
            "my_db_password_2025",
            "P@ssw0rd!",
            "a",  # Односимвольный пароль
            "12345678",  # Только цифры
        ]

        for password in valid_passwords:
            assert validate_db_password(password) == password

    def test_validate_db_password_invalid(self):
        """Проверяет, что некорректные пароли вызывают исключение."""
        # Тестирование некорректных паролей
        invalid_passwords = [
            "",  # Пустая строка
            "   ",  # Только пробелы
            None,  # None
        ]

        for password in invalid_passwords:
            with pytest.raises(InvalidDbPasswordException):
                validate_db_password(password)

    def test_validate_db_name_valid(self):
        """Проверяет, что корректное имя базы данных проходит валидацию."""
        # Тестирование корректных имен баз данных
        valid_db_names = [
            "mydb",
            "production_db",
            "test_database",
            "app-data",
            "analytics_db_2025",
        ]

        for db_name in valid_db_names:
            assert validate_db_name(db_name) == db_name

    def test_validate_db_name_invalid(self):
        """Проверяет, что некорректные имена баз данных вызывают исключение."""
        # Тестирование некорректных имен баз данных
        invalid_db_names = [
            "",  # Пустая строка
            "   ",  # Только пробелы
            None,  # None
        ]

        for db_name in invalid_db_names:
            with pytest.raises(InvalidDbNameException):
                validate_db_name(db_name)

    def test_validate_db_port_valid(self):
        """Проверяет, что корректный порт проходит валидацию."""
        # Тестирование корректных портов
        # Тестирование граничных значений и нескольких значений в середине диапазона
        valid_ports = [
            1,  # Минимальный допустимый порт
            1024,  # Порты выше привилегированных
            5432,  # Типичный порт PostgreSQL
            3306,  # Типичный порт MySQL
            1521,  # Типичный порт Oracle
            65535,  # Максимальный допустимый порт
        ]

        for port in valid_ports:
            assert validate_db_port(port) == port

    def test_validate_db_port_invalid(self):
        """Проверяет, что некорректные порты вызывают исключение."""
        # Тестирование некорректных портов
        # Порты ниже минимального и выше максимального значения
        invalid_ports = [
            0,  # Ниже минимального значения
            -1,  # Отрицательный порт
            65536,  # Выше максимального значения
            1000000,  # Очень большой порт
        ]

        for port in invalid_ports:
            with pytest.raises(InvalidDbPortException):
                validate_db_port(port)

    def test_validate_db_port_type_invalid(self):
        """Проверяет, что передача нецелочисленного значения вызывает ошибку."""
        # Тестирование нецелочисленных значений
        # Хотя функция ожидает int, мы проверяем, что нецелые значения
        # ведут к ошибкам на уровне Python
        invalid_types = [
            "8080",  # Строка
            "abc",  # Буквы
            80.5,  # Дробное число
            None,  # None
            [],  # Список
            {},  # Словарь
        ]

        for port in invalid_types:
            with pytest.raises(InvalidDbPortException):
                validate_db_port(port)
