import requests

resource = requests.get("https://playground.learnqa.ru/api/long_redirect")

print(resource.history)



print(resource.history[0].url)
print(resource.history[1].url)
print(resource.url)

print(resource.history[0].status_code)
print(resource.history[1].status_code)
print(resource.status_code)
