from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_by_name(response: Response, name, expected_value, error_message):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name in response_dict, f"Response doesn't have key '{name}'"
        assert response_dict[name] == expected_value, error_message

