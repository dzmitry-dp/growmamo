import os
import ujson
import json

def read_file(filename):
    # Проверка наличия файла
    if filename not in os.listdir():
        # Создание содержимого файла
        wifi_data = {
            "login": "",
            "password": ""
        }
        
        # Запись содержимого в файл
        with open(filename, "w") as file:
            ujson.dump(wifi_data, file)
        print(f"Файл {filename} создан.")
        return None, None
    else:
        print(f"Файл {filename} уже существует.")
        with open(filename, 'r') as file:
            file_data = file.read().strip()
            wifi_data = json.loads(file_data)
        return wifi_data['login'], wifi_data['password']
