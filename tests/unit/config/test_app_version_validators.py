"""
Тесты для валидации версии приложения в классе AppConfig.

Этот модуль содержит тесты для проверки валидации формата версии приложения
в классе AppConfig. Тесты проверяют корректность формата версии в соответствии
с требованиями YEAR.MONTH.PATCH и обработку различных сценариев ошибок.
"""

import pytest

from config.validators import validate_app_version
from config.exceptions import InvalidVersionFormatException, InvalidVersionYearException, InvalidVersionMonthException


class TestAppConfigVersionValidation:
    """Тестовый класс для проверки валидации версии приложения."""
    
    def test_valid_version_format(self):
        """Проверяет, что корректный формат версии проходит валидацию."""

        # Тестирование корректных форматов версий
        valid_versions = [
            "2025.01.1",
            "2025.12.1",
            "2025.01.5",
            "2026.1.10",  # Год в пределах допустимого диапазона
            "2025.6.100"  # Большие номера патчей
        ]

        for version in valid_versions:
            valid_version: str = validate_app_version(version)
            assert valid_version == version

    def test_invalid_version_format(self):
        """Проверяет, что некорректный формат версии вызывает исключение."""

        # Тестирование различных некорректных форматов
        invalid_formats = [
            "25.12.1",      # Год из двух цифр
            "2025.1",       # Отсутствует номер патча
            "2025",         # Только год
            "2025.13",      # Только год и месяц
            "abc.def.ghi",  # Буквы вместо цифр
            "2025-12-1",    # Неверные разделители
            "2025/12/1",    # Другие разделители
            "2025.12.1.1",  # Слишком много компонентов
            "",             # Пустая строка
            "2025.12",      # Отсутствует номер патча
            "2025..1",      # Пропущен номер месяца
            ".12.1",        # Пропущен год
            "2025.12."      # Пропущен номер патча
            "2025.-1.1"     # Отрицательный месяц
        ]

        for version in invalid_formats:
            with pytest.raises(InvalidVersionFormatException):
                validate_app_version(version)
    
    def test_invalid_version_year(self):
        """Проверяет, что недопустимый год в версии вызывает исключение."""

        # Тестирование годов вне допустимого диапазона
        # Допустимый диапазон: от VERSION_MIN_YEAR (2025) до 2026 (2025 + 1)
        invalid_years = [
            "2024.12.1",  # Год меньше минимального
            "2023.1.1",   # Значительно меньший год
            "2027.1.1",   # Год больше максимально допустимого (2025 + 1)
            "2028.12.1"   # Значительно больший год
        ]

        for version in invalid_years:
            with pytest.raises(InvalidVersionYearException):
                validate_app_version(version)
    
    def test_valid_version_year_range(self):
        """Проверяет, что года в допустимом диапазоне проходят валидацию."""
            
        # Тестирование годов в допустимом диапазоне
        # Допустимый диапазон: от VERSION_MIN_YEAR (2025) до 2026 (2025 + 1)
        valid_years = [
            "2025.1.1",  # Минимально допустимый год
            "2026.12.1"  # Максимально допустимый год (текущий год + 1)
        ]

        for version in valid_years:
            valid_version: str = validate_app_version(version)
            assert valid_version == version
    
    def test_invalid_version_month(self):
        """Проверяет, что недопустимый месяц в версии вызывает исключение."""
            
        # Тестирование месяцев вне допустимого диапазона (1-12)
        invalid_months = [
            "2025.0.1",   # Месяц 0
            "2025.13.1",  # Месяц 13
            "2025.14.1",  # Месяц 14
        ]

        for version in invalid_months:
            with pytest.raises(InvalidVersionMonthException):
                validate_app_version(version)
    
    def test_valid_version_month_range(self):
        """Проверяет, что месяцы в допустимом диапазоне проходят валидацию."""
            
        # Тестирование месяцев в допустимом диапазоне (1-12)
        # Тестирование первого, последнего и нескольких месяцев в середине
        valid_months = [
            "2025.1.1",   # Январь
            "2025.6.1",   # Июнь
            "2025.12.1"   # Декабрь
        ]

        for version in valid_months:
            valid_version: str = validate_app_version(version)
            assert valid_version == version
    
    def test_version_validation_with_different_patch_numbers(self):
        """Проверяет, что различные номера патчей не влияют на валидацию."""
            
        # Тестирование различных номеров патчей
        patch_versions = [
            "2025.1.1",    # Маленький номер
            "2025.1.10",   # Двузначный номер
            "2025.1.100",  # Трехзначный номер
            "2025.1.999"   # Большой номер
        ]

        for version in patch_versions:
            valid_version: str = validate_app_version(version)
            assert valid_version == version
    
    def test_version_validation_with_leading_zeros(self):
        """Проверяет, что ведущие нули в месяце не влияют на валидацию."""
            
        # Тестирование месяцев с ведущими нулями
        versions_with_zeros = [
            "2025.01.1",  # Январь с ведущим нулем
            "2025.02.1",  # Февраль с ведущим нулем
            "2025.09.1",  # Сентябрь с ведущим нулем
        ]

        for version in versions_with_zeros:
            valid_version: str = validate_app_version(version)
            assert valid_version == version
    
    def test_version_validation_edge_cases(self):
        """Проверяет граничные случаи валидации версии."""

        # Тестирование различных граничных случаев
        edge_cases = [
            "2025.1.0",   # Нулевой номер патча
            "2025.1.00",  # Несколько нулей в номере патча
            "2025.01.01", # Ведущие нули в месяце и патче
        ]

        for version in edge_cases:
            valid_version: str = validate_app_version(version)
            assert valid_version == version
