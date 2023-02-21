from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.cookies import Cookies
from lib.headers import Headers
from lib.keys import Keys
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_delete_user_with_id_2(self):

        data = {
            f'{Keys.email}': "vinkotov@example.com",
            f'{Keys.password}': "1234"
        }

        response_login = MyRequests.post("/user/login", data)

        auth_sid = self.get_cookie(response_login, Cookies.auth_sid)
        token = self.get_header(response_login, Headers.x_csrf_token)
        user_id = self.get_json_value(response_login, Keys.user_id)

        delete_response = MyRequests.delete("/user/" + str(user_id),
                                            headers={Headers.x_csrf_token: token},
                                            cookies={Cookies.auth_sid: auth_sid})

        assert delete_response.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",\
            "Incorrect error message"
        Assertions.assert_status_code(delete_response, 400)

    def test_delete_user(self):
        login_data = self.sign_up()
        login_response = MyRequests.post("/user/login/", data=login_data)

        auth_sid = self.get_cookie(login_response, Cookies.auth_sid)
        token = self.get_header(login_response, Headers.x_csrf_token)
        user_id = self.get_json_value(login_response, Keys.user_id)

        delete_response = MyRequests.delete("/user/" + str(user_id),
                                            headers={Headers.x_csrf_token: token},
                                            cookies={Cookies.auth_sid: auth_sid})

        Assertions.assert_status_code(delete_response, 200)

        response_user = MyRequests.get("/user/" + str(user_id),
                                       headers={f"{Headers.x_csrf_token}": token},
                                       cookies={f"{Cookies.auth_sid}": auth_sid})

        Assertions.assert_status_code(response_user, 404)
        assert response_user.text == "User not found", "User exist after deleting "

    def test_delete_other_user(self):
        login_data = self.sign_up()
        login_response = MyRequests.post("/user/login/", data=login_data)

        auth_sid = self.get_cookie(login_response, Cookies.auth_sid)
        token = self.get_header(login_response, Headers.x_csrf_token)
        user_id = self.get_json_value(login_response, Keys.user_id)

        other_user_id = "62640"

        response_delete = MyRequests.delete("/user/" + str(other_user_id),
                                            headers={Headers.x_csrf_token: token},
                                            cookies={Cookies.auth_sid: auth_sid})

        Assertions.assert_status_code(response_delete, 422)
        # some error
        # assert response_delete.text == "some error ", "Incorrect error"

        response_user = MyRequests.get("/user/" + str(user_id),
                                       headers={f"{Headers.x_csrf_token}": token},
                                       cookies={f"{Cookies.auth_sid}": auth_sid})

        Assertions.assert_status_code(response_user, 200)
