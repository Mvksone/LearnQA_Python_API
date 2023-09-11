from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Edit user testcases")
class TestUserEdit(BaseCase):
    @allure.description("This edit just created user")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data =self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test edit user without auth")
    def test_edit_user_without_auth(self):
        new_name = "Changed Name1"
        response1 = MyRequests.put(
            f"/user/2",
            data={"firstName": new_name}
        )
        print(response1.content)
        Assertions.assert_code_status(response1, 400)
        assert response1.content.decode(
                "utf-8") == f"Auth token not supplied", f"Unexpected response content"

    @allure.description("This test edit new user with auth as another user")
    def test_edit_new_user_with_auth_another_user(self):
         # REGISTER USER_1
         register_data =self.prepare_registration_data()
         response1 = MyRequests.post("/user", data=register_data)

         Assertions.assert_code_status(response1, 200)
         Assertions.assert_json_has_key(response1, "id")

         new_user_email = register_data['email']
         new_user_password = register_data['password']


         # LOGIN NEW USER_1
         new_user_reg_data = {
             "email": new_user_email,
             "password": new_user_password
         }
         response2 = MyRequests.post("/user/login", data=new_user_reg_data)
         new_user_auth_sid = self.get_cookie(response2, "auth_sid")
         new_user_token = self.get_header(response2, "x-csrf-token")


         # REG NEW USER_2
         register_data =self.prepare_registration_data()
         response3 = MyRequests.post("/user", data=register_data)

         print(response3.content)
         Assertions.assert_code_status(response3, 200)
         Assertions.assert_json_has_key(response3, "id")

         new_user2_email = register_data['email']
         new_user2_password = register_data['password']
         new_user2_id = self.get_json_value(response3, "id")

         # EDIT USER_2 WITH USER_1 DATA
         new_name = "Changed Name"
         response4 = MyRequests.put(
             f"/user/{new_user2_id}",
             headers={"x-csrf-token": new_user_token},
             cookies={"auth_sid": new_user_auth_sid},
             data={"firstName": new_name}
         )
         Assertions.assert_code_status(response4, 200)

         # LOGIN USER_2
         data ={
             'email': new_user2_email,
             'password': new_user2_password
         }

         response5 = MyRequests.post("/user/login", data=data)
         new_user2_auth_sid = self.get_cookie(response5, "auth_sid")
         new_user2_token = self.get_header(response5, "x-csrf-token")

        # GET USER_2 DATA
         response6 = MyRequests.get(
              f"/user/{new_user2_id}",
              headers={"x-csrf-token": new_user2_token},
              cookies={"auth_sid": new_user2_auth_sid}
          )
         edited_user_email = self.get_json_value(response6, "firstName")
         assert edited_user_email == new_name, f"The firstName parameter of user2 has not changed"

    @allure.description("This test edit wrong email with auth the same user")
    def test_edit_wrong_email_with_auth_same_user(self):
    # REGISTER NEW USER
        register_data =self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

    # LOGIN NEW USER 1
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

    # EDIT
        new_email = "wrongemail"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content {response3.content}"

    @allure.description("This test edit wrong firstName with auth the same user")
    def test_edit_wrong_firstName_with_auth_same_user(self):
    # REGISTER NEW USER
        register_data =self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

    # LOGIN NEW USER 1
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

    # EDIT
        new_name = "a"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 400)
        error = self.get_json_value(response3, "error")
        assert error == f"Too short value for field firstName", f"Unexpected response content {response3.content}"