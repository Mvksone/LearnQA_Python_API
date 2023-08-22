from json.decoder import JSONDecodeError
import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
first_responce = response.history[0]
second_responce = response

print(first_responce.url)
print(second_responce.url)
