import requests
class TestEx11:
    def test_checkCookie(self):

        cookieResponse = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print(cookieResponse.cookies)

        cookieName = "HomeWork"
        cookieValue = "hw_value"

        assert cookieName in cookieResponse.cookies, "There is no 'HomeWork' cookies in the response"
        assert cookieResponse.cookies.get(cookieName) == cookieValue,  "Incorrect 'HomeWork' cookie value "







