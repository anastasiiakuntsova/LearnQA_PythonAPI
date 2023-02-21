import pytest
import requests
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.cookies import Cookies
from lib.headers import Headers
from lib.keys import Keys
from lib.my_requests import MyRequests


@allure.epic("Authorisation cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookie",
        "no_token"
    ]

    @allure.description("Successfully auth by email and password")
    def test_auth_user(self):

        data = {
            Keys.email: 'vinkotov@example.com',
            Keys.password: '1234'
        }
        login_response = MyRequests.post("/user/login/", data)

        token = self.get_header(login_response, Headers.x_csrf_token)
        auth_sid = self.get_cookie(login_response, Cookies.auth_sid)
        user_id_from_login = self.get_json_value(login_response, Keys.user_id)

        auth_response = MyRequests.get("/user/auth/",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid}
                                       )

        Assertions.assert_json_has_key(auth_response, Keys.user_id)

        Assertions.assert_json_by_name(
            auth_response,
            "user_id",
            user_id_from_login,
            "User id from auth method is not equal to user id from check method"
        )

    @allure.description("Checking auth status without sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        data = {
            Keys.email: 'vinkotov@example.com',
            Keys.password: '1234'
        }
        login_response = MyRequests.post("/user/login/", data)

        token = self.get_header(login_response, Headers.x_csrf_token)
        auth_sid = self.get_cookie(login_response, Cookies.auth_sid)

        if condition == "no_cookie":
            response_auth = MyRequests.get("/user/auth",
                                           headers={Headers.x_csrf_token: token})
        else:
            response_auth = MyRequests.get("/user/auth",
                                           cookies={Cookies.auth_sid: auth_sid})

        Assertions.assert_json_has_key(response_auth, Keys.user_id)
        assert self.get_json_value(response_auth, Keys.user_id) == 0, f"User is authorized with condition {condition}"

