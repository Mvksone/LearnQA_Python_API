import requests

def output_params(method, j, response):
    print(f"Метод: {method}")
    print(f"Параметр: {j}")
    print(f"Статус код: {response.status_code}")
    print(f"Текст ответа: {response.text}")
    print("--------------------")


#1
def random_method():
    response = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type')
    print(response.text)
    print("--------------------")

#2
def other_method():
    response = requests.head('https://playground.learnqa.ru/ajax/api/compare_query_type')
    print(response.text)
    print("--------------------")

#3
def get_with_params():
    params = {"method": "GET"}
    response = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params=params)
    print(response.text)
    print("--------------------")

#4
def all_methods():

    methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
    for method in methods:
        if method == "GET":
            for param in methods:
                params = {"method": param}
                response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=params)
                output_params(method, param, response)
        elif method == "POST":
            for param in methods:
                data = {"method": param}
                response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=data)
                output_params(method, param, response)
        elif method == "PUT":
            for param in methods:
                data = {"method": param}
                response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=data)
                output_params(method, param, response)
        elif method == "DELETE":
            for param in methods:
                data = {"method": param}
                response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=data)
                output_params(method, param, response)
        elif method == "HEAD":
            for param in methods:
                data = {"method": param}
                response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data=data)
                output_params(method, param, response)
        elif method == "OPTIONS":
            for param in methods:
                data = {"method": param}
                response = requests.options("https://playground.learnqa.ru/ajax/api/compare_query_type", data=data)
                output_params(method, param, response)
        elif method == "PATCH":
            for param in methods:
                data = {"method": param}
                response = requests.patch("https://playground.learnqa.ru/ajax/api/compare_query_type", data=data)
                output_params(method, param, response)
random_method()
other_method()
get_with_params()

all_methods()
