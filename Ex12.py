import requests
class TestEx12:
    def test_checkHeader(self):

        headerResponse = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(headerResponse.headers)

        headerName = "x-secret-homework-header"
        headerValue = "Some secret value"

        assert headerName in headerResponse.headers, f"There is no {headerName} header in the response"
        assert headerResponse.headers.get(headerName) == headerValue,  f"Incorrect  {headerName} cookie value"







