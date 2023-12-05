import requests

# Создание объявления
response = requests.post("http://127.0.0.1:5000/ads",
                         json={"name": "S_first_ad",
                               "title": "first ad is for apartment selling",
                               "description": "first ad is for apartment selling - it's a very good flat"},
                         )
print("-----Создание объявления-----")
print(response.status_code)
print(response.text)
print("-----------------------------")

# Чтение объявления
response = requests.get("http://127.0.0.1:5000/ads/1",)
print("------Чтение объявления------")
print(response.status_code)
print(response.text)
print("-----------------------------")

# Изменение объявления
response = requests.patch("http://127.0.0.1:5000/ads/1", json={"title": "first ad is for apartment tenancy"}, )
print("-----Изменение объявления----")
print(response.status_code)
print(response.text)
print("-----------------------------")

# Удаление объявления
response = requests.delete("http://127.0.0.1:5000/ads/1",)
print("-----Удаление объявления-----")
print(response.status_code)
print(response.text)
print("-----------------------------")
