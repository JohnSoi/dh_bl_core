"""
Тесты для вспомогательных функций работы со строками.
"""

from utils.str import camel_to_snake_case


class TestCamelToSnakeCase:
    """Тестовый класс для проверки функции camel_to_snake_case."""
    
    def test_basic_camel_case(self):
        """Тест базового преобразования camelCase в snake_case."""
        assert camel_to_snake_case('camelCase') == 'camel_case'
        assert camel_to_snake_case('helloWorld') == 'hello_world'
        assert camel_to_snake_case('simpleTest') == 'simple_test'
    
    def test_multiple_capital_letters(self):
        """Тест преобразования строк с несколькими заглавными буквами подряд."""
        assert camel_to_snake_case('getHTTPResponse') == 'get_http_response'
        assert camel_to_snake_case('parseXMLData') == 'parse_xml_data'
        assert camel_to_snake_case('sendHTTPRequest') == 'send_http_request'
        assert camel_to_snake_case('iOSApp') == 'i_os_app'
    
    def test_start_with_capital_letter(self):
        """Тест преобразования строк, начинающихся с заглавной буквы."""
        assert camel_to_snake_case('CamelCase') == 'camel_case'
        assert camel_to_snake_case('XMLHttpRequest') == 'xml_http_request'
        assert camel_to_snake_case('HTTPClient') == 'http_client'
        assert camel_to_snake_case('APIService') == 'api_service'
    
    def test_with_numbers(self):
        """Тест преобразования строк, содержащих цифры."""
        assert camel_to_snake_case('version2') == 'version2'
        assert camel_to_snake_case('version2Word') == 'version2_word'
        assert camel_to_snake_case('number10Test3') == 'number10_test3'
        assert camel_to_snake_case('test2B') == 'test2_b'
    
    def test_single_words(self):
        """Тест преобразования одиночных слов."""
        assert camel_to_snake_case('word') == 'word'
        assert camel_to_snake_case('Word') == 'word'
        assert camel_to_snake_case('X') == 'x'
        assert camel_to_snake_case('a') == 'a'
    
    def test_edge_cases(self):
        """Тест граничных случаев."""
        assert camel_to_snake_case('') == ''
        assert camel_to_snake_case('a') == 'a'
        assert camel_to_snake_case('AA') == 'aa'
        assert camel_to_snake_case('Aa') == 'aa'
        assert camel_to_snake_case('aA') == 'a_a'
        assert camel_to_snake_case('aAB') == 'a_ab'
    
    def test_with_existing_underscores(self):
        """Тест обработки строк, уже содержащих подчеркивания."""
        # Функция не предназначена для обработки подчеркиваний,
        # но важно понимать ее поведение
        assert camel_to_snake_case('already_snake_case') == 'already_snake_case'
        assert camel_to_snake_case('mixedCamel_Snake') == 'mixed_camel_snake'
        assert camel_to_snake_case('test_API_v2') == 'test_api_v2'
    
    def test_special_camel_cases(self):
        """Тест специальных случаев camelCase."""
        assert camel_to_snake_case('userID') == 'user_id'
        assert camel_to_snake_case('HTMLParser') == 'html_parser'
        assert camel_to_snake_case('iPhone') == 'i_phone'
        assert camel_to_snake_case('URLHandler') == 'url_handler'
        assert camel_to_snake_case('CSSRule') == 'css_rule'
