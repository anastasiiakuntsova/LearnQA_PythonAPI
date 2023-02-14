import requests
import time


keyStatus = "status"
keyToken = "token"
keySeconds = "seconds"
keyResult = "result"

createTaskResponse = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

createTaskJson = createTaskResponse.json()
token = createTaskJson[keyToken]
seconds = createTaskJson[keySeconds]

getStatusResponse = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token":token})

getStatusJson = getStatusResponse.json()
assert getStatusJson[keyStatus] == "Job is NOT ready"

time.sleep(seconds)

finishedTaskResponse = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token":token})
finishedTaskJson = finishedTaskResponse.json()

assert finishedTaskJson[keyStatus] == "Job is ready"

if keyStatus in finishedTaskJson:
    print("there is key 'result' in response , value is " + finishedTaskJson[keyResult])
else:
    print("there is no key 'result' in response")





