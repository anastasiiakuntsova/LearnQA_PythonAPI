import string

import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.cookies import Cookies
from lib.headers import Headers
from lib.keys import Keys
from lib.my_requests import MyRequests
import random


class TestUserEdit(BaseCase):
    parameterNames = [Keys.password, Keys.username, Keys.firstName, Keys.lastName, Keys.email]

    def test_edit_just_created_user(self):
        # sign up
        sign_up_data = self.prepare_registratiotion_data()
        sign_up_response = MyRequests.post("/user/", data=sign_up_data)
        Assertions.assert_status_code(sign_up_response, 200)
        Assertions.assert_json_has_key(sign_up_response, Keys.id)

        email = sign_up_data[Keys.email]
        first_name = sign_up_data[Keys.firstName]
        password = sign_up_data[Keys.password]
        user_id = self.get_json_value(sign_up_response, Keys.id)

        # login

        login_data = {
            Keys.email: email,
            Keys.password: password
        }

        login_response = MyRequests.post("/user/login/", data=login_data)
        auth_sid = self.get_cookie(login_response, Cookies.auth_sid)
        token = self.get_header(login_response, Headers.x_csrf_token)

        # change name

        new_name = "testName"

        user_put_response = MyRequests.put("/user/" + user_id,
                                           headers={Headers.x_csrf_token: token},
                                           cookies={Cookies.auth_sid: auth_sid},
                                           data={Keys.firstName: new_name})

        Assertions.assert_status_code(user_put_response, 200)

        # get data and check

        user_get_response = MyRequests.get("/user/" + user_id,
                                           headers={Headers.x_csrf_token: token},
                                           cookies={Cookies.auth_sid: auth_sid})

        Assertions.assert_json_by_name(user_get_response, Keys.firstName, new_name,
                                       f"Incorrect user name. After changing should be {new_name}")

    @pytest.mark.parametrize('param_name', parameterNames)
    def test_change_not_auth_user(self, param_name):
        user_id = "62640"

        new_value = ''.join(random.choice(string.ascii_lowercase) for i in range(10))

        user_put_response = MyRequests.put("/user/" + user_id, data={param_name: new_value})

        assert user_put_response.text == "Auth token not supplied", "Incorrect error message"
        Assertions.assert_status_code(user_put_response, 400)

        incorrect_auth_sid = "gc151707510ffcb9da9dc2d22bdca620a6ea6af64ded3c205989ad664b09f48c"
        incorrect_token = "ac4c60483267e62fc5e2d7ec41b7c05961d305bea6ea6af64ded3c205989ad664b09f48c"

        user_put_response_with_incorrect_token = MyRequests.put("/user/" + user_id,
                                                                headers={Headers.x_csrf_token: incorrect_token},
                                                                cookies={Cookies.auth_sid: incorrect_auth_sid},
                                                                data={param_name: new_value})

        assert user_put_response_with_incorrect_token.text == "Auth token not supplied", "Incorrect error message"
        Assertions.assert_status_code(user_put_response, 400)

    @pytest.mark.parametrize('param_name', parameterNames)
    def test_change_other_signed_in_user(self, param_name):
        data = {
            f'{Keys.email}': "learnqatpporsetnb@example.com",
            f'{Keys.password}': "123"
        }

        response_login = MyRequests.post("/user/login", data)
        auth_sid = self.get_cookie(response_login, Cookies.auth_sid)
        token = self.get_header(response_login, Headers.x_csrf_token)
        user_id = self.get_json_value(response_login, Keys.user_id)

        response_user_data = MyRequests.get("/user/" + str(user_id),
                                            headers={Headers.x_csrf_token: token},
                                            cookies={Cookies.auth_sid: auth_sid})
        correct_value = self.get_json_value(response_user_data, param_name)

        other_user_id = "62640"

        incorrect_value = ''.join(random.choice(string.ascii_lowercase) for i in range(10))

        user_put_response_with_incorrect_user_id = MyRequests.put("/user/" + other_user_id,
                                                                  headers={Headers.x_csrf_token: token},
                                                                  cookies={Cookies.auth_sid: auth_sid},
                                                                  data={param_name: incorrect_value})

        # some expected message
        # assert user_put_response_with_incorrect_user_id.text == "Auth token not supplied", "Incorrect error message"
        Assertions.assert_status_code(user_put_response_with_incorrect_user_id, 422)

        response_get_user_data = MyRequests.get("/user/" + str(user_id),
                                                headers={Headers.x_csrf_token: token},
                                                cookies={Cookies.auth_sid: auth_sid})

        Assertions.assert_json_by_name(response_get_user_data, param_name, correct_value,
                                       f"Incorrect parametr. Parametr shouldn't changed with incorrect user id and "
                                       f"should be {correct_value}")

    def test_change_to_incorrect_email(self):
        correct_email = "learnqatpporsetnb@example.com"
        data = {
            Keys.email: correct_email,
            Keys.password: "123"
        }

        response_login = MyRequests.post("/user/login", data)
        auth_sid = self.get_cookie(response_login, Cookies.auth_sid)
        token = self.get_header(response_login, Headers.x_csrf_token)
        user_id = self.get_json_value(response_login, Keys.user_id)

        incorrect_email = ''.join(random.choice(string.ascii_lowercase) for i in range(10)) + "example.com"

        user_put_response_with_incorrect_email = MyRequests.put("/user/" + str(user_id),
                                                                headers={Headers.x_csrf_token: token},
                                                                cookies={Cookies.auth_sid: auth_sid},
                                                                data={Keys.email: incorrect_email})

        assert user_put_response_with_incorrect_email.text == "Invalid email format", "Incorrect error message"
        Assertions.assert_status_code(user_put_response_with_incorrect_email, 400)

        response_get_user_data = MyRequests.get("/user/" + str(user_id),
                                                headers={Headers.x_csrf_token: token},
                                                cookies={Cookies.auth_sid: auth_sid})

        Assertions.assert_json_by_name(response_get_user_data, Keys.email, correct_email,
                                       f"Incorrect email. Email shouldn't changed and should be {correct_email}")

    def test_incorrect_changing_first_name(self):
        data = {
            Keys.email: "learnqatpporsetnb@example.com",
            Keys.password: "123"
        }

        response_login = MyRequests.post("/user/login", data)
        auth_sid = self.get_cookie(response_login, Cookies.auth_sid)
        token = self.get_header(response_login, Headers.x_csrf_token)
        user_id = self.get_json_value(response_login, Keys.user_id)

        response_user_data = MyRequests.get("/user/" + str(user_id),
                                            headers={Headers.x_csrf_token: token},
                                            cookies={Cookies.auth_sid: auth_sid})
        correct_first_name = self.get_json_value(response_user_data, Keys.firstName)

        incorrect_name = "t"

        user_put_response_with_incorrect_name = MyRequests.put("/user/" + str(user_id),
                                                               headers={Headers.x_csrf_token: token},
                                                               cookies={Cookies.auth_sid: auth_sid},
                                                               data={Keys.firstName: incorrect_name})

        error = self.get_json_value(user_put_response_with_incorrect_name, "error")

        assert error == "Too short value for field firstName", \
            "Incorrect error message"
        Assertions.assert_status_code(user_put_response_with_incorrect_name, 400)

        response_get_user_data = MyRequests.get("/user/" + str(user_id),
                                                headers={Headers.x_csrf_token: token},
                                                cookies={Cookies.auth_sid: auth_sid})

        Assertions.assert_json_by_name(response_get_user_data, Keys.firstName, correct_first_name,
                                       f"Incorrect first name. First name shouldn't changed and should be {correct_first_name}")
