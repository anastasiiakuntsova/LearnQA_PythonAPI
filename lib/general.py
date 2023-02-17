import json

from requests import Response


class General:

    @staticmethod
    def check_json_format(response: Response):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"
        return response_dict
