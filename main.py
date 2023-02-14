import requests

print("Hello from Anastasiia")

resource = requests.get("https://playground.learnqa.ru/api/get_text")
print(resource.text)
