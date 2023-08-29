import pytest
import requests

class TestHeaderRequest:

    def test_request_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        headers = response.headers
        print(headers)

        if headers:
            actual_header_name = list(headers.keys())[6]
            actual_header_value = headers.get(actual_header_name)
            print('Header Name is ', actual_header_name)
            print('Header value is ', actual_header_value)

            expected_header_name = "x-secret-homework-header"
            expected_header_value = 'Some secret value'

            assert expected_header_name == actual_header_name , "Actual header name does not match expected "
            assert expected_header_value == actual_header_value, "Actual header name does not match expected "
        else:
            print("Headers not found")

