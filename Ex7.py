import requests

response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)
print(response.status_code)

response = requests.patch("https://playground.learnqa.ru/ajax/api/compare_query_type", data ={"method":"PATCH"})
print(response.text)
print(response.status_code)

response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data ={"method":"POST"})
print(response.text)
print(response.status_code)



list = {"POST", "GET", "PUT", "DELETE"}

print(" ")
for c in list:
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": c})
    print("GET + " + c + " , response.text is " + response.text)
    print("GET + " + c + " , response.status_code is " + str(response.status_code))

print(" ")
for c in list:
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": c})
    print("POST + " + c + " , response.text is " + response.text)
    print("POST + " + c + " , response.status_code is " + str(response.status_code))

print(" ")
for c in list:
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": c})
    print("PUT + " + c + " , response.text is " + response.text)
    print("PUT + " + c + " , response.status_code is " + str(response.status_code))

print(" ")
for c in list:
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": c})
    print("DELETE + " + c + " , response.text is " + response.text)
    print("DELETE + " + c + " , response.status_code is " + str(response.status_code))
