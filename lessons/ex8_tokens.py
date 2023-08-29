import requests
import time
import json


create_task = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
print(create_task.text)
print('---------------')
obj = json.loads(create_task.text)

req_token = obj["token"]
sec = obj["seconds"]

req_response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": req_token})
print(json.loads(req_response.text))
print('---------------')
if json.loads(req_response.text)['status'] == "Job is NOT ready":
    time.sleep(sec)

req_response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": req_token})
if json.loads(req_response.text)['status'] == "Job is ready" and json.loads(req_response.text)['result'] != None:
    print(req_response.text)
    print('---------------')
    print("Успех!")

