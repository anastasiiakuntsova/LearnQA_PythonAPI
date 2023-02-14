import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

print(response.history)



print(response.history[0].url)
print(response.history[1].url)
print(response.url)

print(response.history[0].status_code)
print(response.history[1].status_code)
print(response.status_code)
