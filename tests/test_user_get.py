from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Get user data cases")
class TestUserGet(BaseCase):

    @allure.description("Test get user data without auth")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("Test get user data with auth the same user")
    def test_get_user_details_auth_as_same_user(self):
        data ={
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_metod = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_metod}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("Test get user data with auth as another user")
    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        user_id_from_auth_metod = self.get_json_value(response1, "user_id")

        response3 = MyRequests.get(
            f"/user/{user_id_from_auth_metod-1}",
        )
        Assertions.assert_json_has_key(response3, "username")
        Assertions.assert_json_has_not_key(response3, "email")
        Assertions.assert_json_has_not_key(response3, "firstName")
        Assertions.assert_json_has_not_key(response3, "lastName")