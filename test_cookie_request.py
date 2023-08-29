import pytest
import requests

class TestCookieRequest:
    def test_request_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookies = response.cookies

        if cookies:
            actual_cookie_name = list(cookies.keys())[0]
            actual_cookie_value = cookies.get(actual_cookie_name)
            print('Cookie Name is ', actual_cookie_name)
            print('Сookie value is ', actual_cookie_value)

            expected_cookie_name = "HomeWork"
            expected_cookie_value = 'hw_value'

            assert expected_cookie_name == actual_cookie_name
            assert expected_cookie_value == actual_cookie_value
        else:
            print("Cookie not found")

