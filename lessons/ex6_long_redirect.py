from json.decoder import JSONDecodeError
import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
hist = response.history

for i in range(len(hist)):
    print(hist[i].url)

finish_responce = response
print(finish_responce.url)
