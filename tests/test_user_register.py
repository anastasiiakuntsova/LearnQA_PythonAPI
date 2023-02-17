import random
import string

import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    parameterNames = ["password", "username", "firstName", "lastName", "email"]

    def test_create_user_successfully(self):
        data = self.prepare_registratiotion_data()

        response_user = MyRequests.post("/user/", data=data)
        Assertions.assert_status_code(response_user, 200)
        Assertions.assert_json_has_key(response_user, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registratiotion_data(email)

        response_user = MyRequests.post("/user/", data=data)
        Assertions.assert_status_code(response_user, 400)
        assert response_user.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            "Unexpected response content"

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registratiotion_data(email)

        response_user = MyRequests.post("/user/", data=data)
        Assertions.assert_status_code(response_user, 400)
        assert response_user.content.decode("utf-8") == f"Invalid email format", \
            "Unexpected response content"

    def test_create_user_with_shortName(self):
        data = self.prepare_registratiotion_data()
        data.update({"username": "r"})

        response_user = MyRequests.post("/user/", data=data)
        Assertions.assert_status_code(response_user, 400)
        assert response_user.content.decode("utf-8") == f"The value of 'username' field is too short", \
            "Unexpected response content"

    def test_create_user_with_shortName(self):
        data = self.prepare_registratiotion_data()
        long_name = ''.join(random.choice(string.ascii_lowercase) for i in range(251))

        data.update({"username": long_name})

        response_user = MyRequests.post("/user/", data=data)
        Assertions.assert_status_code(response_user, 400)
        assert response_user.content.decode("utf-8") == f"The value of 'username' field is too long", \
            "Unexpected response content"

    @pytest.mark.parametrize('param_name', parameterNames)
    def test_create_user_without_parameter(self, param_name):
        data = self.prepare_registratiotion_data()
        data.update({param_name: ""})

        response_user = MyRequests.post("/user/", data=data)
        Assertions.assert_status_code(response_user, 400)
        assert response_user.content.decode("utf-8") == f"The value of '{param_name}' field is too short", \
            "Unexpected response content"
