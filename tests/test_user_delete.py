from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Delete users cases")
class TestUserDelete(BaseCase):
    @allure.description("This test successfully deleting an authorized user")
    def test_delete_user_auth(self):
        #LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.post("/user/login", data=data)
        user_id = self.get_json_value(response, "user_id")
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        Assertions.assert_code_status(response, 200)

        #DELETE
        response1 = MyRequests.delete(f"/user/{user_id}",
                    headers={"x-csrf-token": token},
                    cookies={"auth_sid": auth_sid}
                    )
        Assertions.assert_code_status(response1, 400)
        assert response1.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", f"Unexpected response content {response.content}"

    @allure.story("Test deleting a just create user")
    def test_delete_just_create_user(self):
        with allure.step("Registration user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step("Login user"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")
            Assertions.assert_code_status(response1, 200)

        with allure.step("Delete just reg user"):
            response3 = MyRequests.delete(f"/user/{user_id}",
                        headers={"x-csrf-token": token},
                        cookies={"auth_sid": auth_sid}
                        )
            Assertions.assert_code_status(response3, 200)

        with allure.step("Check user data"):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
            )

            Assertions.assert_code_status(response3, 200)
            assert response4.content.decode(
                "utf-8") == f"User not found", f"Unexpected response content {response4.content}"

    @allure.story("Story: Attempt to delete a new user with auth under a another user")
    def test_delete_new_user_with_auth_another_user(self):
        with allure.step("Reg user 1"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            user1_email = register_data['email']
            user1_password = register_data['password']
            #user1_id = self.get_json_value(response1, "id")

        with allure.step("Login user 1"):
            new_user_reg_data = {
                "email": user1_email,
                "password": user1_password
            }
            response2 = MyRequests.post("/user/login", data=new_user_reg_data)
            user1_auth_sid = self.get_cookie(response2, "auth_sid")
            user1_token = self.get_header(response2, "x-csrf-token")

        with allure.step("Reg user 2"):
            register_data2 = self.prepare_registration_data()
            response3 = MyRequests.post("/user", data=register_data2)

            Assertions.assert_code_status(response3, 200)
            Assertions.assert_json_has_key(response3, "id")

            new_user2_email = register_data2['email']
            new_user2_password = register_data2['password']
            new_user2_id = self.get_json_value(response3, "id")

        with allure.step("Delete user 2 with user 1 data"):
            response4 = MyRequests.delete(
                f"/user/{new_user2_id}",
                headers={"x-csrf-token": user1_token},
                cookies={"auth_sid": user1_auth_sid}
            )
            Assertions.assert_code_status(response4, 200)

        with allure.step("Login user 2"):
            data = {
                'email': new_user2_email,
                'password': new_user2_password
            }

            response5 = MyRequests.post("/user/login", data=data)

            new_user2_auth_sid = self.get_cookie(response5, "auth_sid")
            new_user2_token = self.get_header(response5, "x-csrf-token")

        with allure.step("Check user 2 data"):
            response6 = MyRequests.get(
                f"/user/{new_user2_id}",
                headers={"x-csrf-token": new_user2_token},
                cookies={"auth_sid": new_user2_auth_sid}
            )
            print(response6.content)
            Assertions.assert_json_has_not_key(response6, 'id')
            Assertions.assert_json_has_not_key(response6, 'email')
            Assertions.assert_json_has_not_key(response6, 'firstName')
            Assertions.assert_json_has_not_key(response6, 'lastName')






