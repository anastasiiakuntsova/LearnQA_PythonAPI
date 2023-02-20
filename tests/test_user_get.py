from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.cookies import Cookies
from lib.headers import Headers
from lib.keys import Keys
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    def test_user_get_details_not_auth(self):
        response_user = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response_user, Keys.username)
        Assertions.assert_json_doesnt_have_key(response_user, Keys.email,
                                               Keys.firstName, Keys.lastName)

    def test_user_get_details_auth_as_same_user(self):
        data = {
            f'{Keys.email}': "vinkotov@example.com",
            f'{Keys.password}': "1234"
        }

        response_login = MyRequests.post("/user/login", data)
        auth_sid = self.get_cookie(response_login, Cookies.auth_sid)
        token = self.get_header(response_login, Headers.x_csrf_token)
        user1_response_login = self.get_json_value(response_login, Keys.user_id)

        response_user = MyRequests.get("/user/" + str(user1_response_login),
                                       headers={f"{Headers.x_csrf_token}": token},
                                       cookies={f"{Cookies.auth_sid}": auth_sid})

        Assertions.assert_json_has_key(response_user, Keys.username,
                                       Keys.email, Keys.firstName, Keys.lastName)

    def test_user_get_details_with_other_id(self):
        data = {
            f'{Keys.email}': "vinkotov@example.com",
            f'{Keys.password}': "1234"
        }

        response_login = MyRequests.post("/user/login", data)
        auth_sid = self.get_cookie(response_login, Cookies.auth_sid)
        token = self.get_header(response_login, Headers.x_csrf_token)
        incorrect_user_id = "1"

        response_user = MyRequests.get("/user/" + incorrect_user_id,
                                       headers={f"{Headers.x_csrf_token}": token},
                                       cookies={f"{Cookies.auth_sid}": auth_sid})

        Assertions.assert_json_has_key(response_user, Keys.username)
        Assertions.assert_json_doesnt_have_key(response_user, Keys.email,
                                               Keys.firstName, Keys.lastName)

