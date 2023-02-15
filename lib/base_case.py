import json

from requests import Response


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"There is no cookie whith the name  {cookie_name} in response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"There is no header with the name  {headers_name} in response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name in response_dict, f"Response doesn't have key '{name}'"

        return response_dict[name]
