from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest


class TestUserRegister(BaseCase):

    missing_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('condition', missing_params)
    def test_create_user_without_any_param(self, condition):
        if condition == 'password':
            data = {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
            }
        elif condition == 'username':
            data = {
            'password': '123',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
            }
        elif condition == 'firstName':
            data = {
            'password': '123',
            'username': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
            }
        elif condition == 'lastName':
            data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'email': 'vinkotov@example.com'
            }
        elif condition == 'email':
            data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa'
            }

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}", f"Unexpected response content {response.content}"


    def test_create_user_with_short_username(self):
        username = 'a'
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
                "utf-8") == f"The value of 'username' field is too short", f"Unexpected response content {response.content}"

    def test_create_user_with_long_username(self):
        #username of 253 characters
        username = 'werhazhphsnhvtfsydzlfvpdfcfplbguitheplytwyxevnxhqjlsgtrprfwurhrrnfuvifybtryywqbdddxnzerggxlyzgtxrsbyrvtjzymiicldkrdmqulvafjvebnvcgfnnmlxbyhdtyulctmkvlfhsyqftliszcvuungjltdtwozxcsxdehvwtpctnmrmudxyidtkvwjhrknenxlljsgzgbrgqwtsfvjzgjffhjhcfxxmttgvrkbfnlnyr'
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
                "utf-8") == f"The value of 'username' field is too long", f"Unexpected response content {response.content}"