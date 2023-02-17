import string
import random
from requests import Response
from lib.general import General


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
