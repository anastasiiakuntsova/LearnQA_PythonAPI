from requests import Response
from lib.general import General


class Assertions:
    @staticmethod
    def assert_json_by_name(response: Response, name, expected_value, error_message):
        response_dict = General.check_json_format(response)
        assert name in response_dict, f"Response doesn't have key '{name}'"
        assert response_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, *key):
        response_dict = General.check_json_format(response)
        for some_key in key:
            assert some_key in response_dict, f"Response doesn't have key '{some_key}'"

    @staticmethod
    def assert_status_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}, actual: {response.status_code}"
