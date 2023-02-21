import string
import random

import allure
from requests import Response

from lib.assertions import Assertions
from lib.general import General
from lib.keys import Keys
from lib.my_requests import MyRequests


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"There is no cookie with the name  {cookie_name} in response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"There is no header with the name  {headers_name} in response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        response_dict = General.check_json_format(response)
        assert name in response_dict, f"Response doesn't have key '{name}'"

        return response_dict[name]

    def prepare_registratiotion_data(self, email=None):
        if email is None:
            random_str = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
            email = "learnqa" + random_str + "@example.com"

        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def sign_up(self):
        with allure.step(f"Sign up step"):
            sign_up_data = self.prepare_registratiotion_data()
            sign_up_response = MyRequests.post("/user/", data=sign_up_data)
            Assertions.assert_status_code(sign_up_response, 200)
            Assertions.assert_json_has_key(sign_up_response, Keys.id)

            email = sign_up_data[Keys.email]
            password = sign_up_data[Keys.password]

            login_data = {
                Keys.email: email,
                Keys.password: password
            }

            return login_data


