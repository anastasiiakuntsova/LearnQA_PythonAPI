import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        login_response = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        self.auth_sid = self.get_cookie(login_response, "auth_sid")
        self.token = self.get_header(login_response, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(login_response, "user_id")

    def test_auth_user(self):

        auth_response = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_by_name(
            auth_response,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )
