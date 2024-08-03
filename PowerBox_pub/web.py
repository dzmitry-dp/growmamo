import socket
import json


ports = [80, 5678] # порты, которые будет слушать контроллер в режиме точки доступа

def create_sockets(mamo_ssid = None, home_wifi = None):
    sockets = {}
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not home_wifi:
            if mamo_ssid.active():
                sock.bind((mamo_ssid.ifconfig()[0], port))
                print(f'Listening SSID {mamo_ssid.ifconfig()[0]} on port {port}...')
        else: # если подключен домашний wifi
            sock.bind((home_wifi.ifconfig()[0], port))
            print(f'Listening sta_if ...')
        sock.listen(2)
        sock.setblocking(False)
        sockets[sock] = port
    return sockets

def web_data(socket_1 = 'off', socket_2 = 'off'):
    return "{'header': {'title': 'miniBox'}, 'payload': {'socket_1': " + socket_1 + "," + "'socket_2': " + socket_2 + "}, 'signature': {'from': 'ESP8266 Nodemcu v3/MicroPython v1.23.0', 'firmware': 'v0.0.1'}}"

def handle_post_request(request):
    "Обработка входящего POST-запроса"
    
    def text_to_dict(text):
        "Преобразование входящих данных в dict структуру"
        # Создаем пустой словарь для хранения данных
        data_dict = {}
        # Разбиваем текст на строки
        lines = text.split('\n')
        # Обрабатываем каждую строку
        for line in lines:
            # Игнорируем пустые строки
            if line.strip():
                # Проверяем, содержит ли строка разделитель ': '
                if ': ' in line:
                    # Разделяем строку на ключ и значение по первому вхождению ': '
                    key, value = line.split(': ', 1)
                    # Добавляем ключ и значение в словарь
                    data_dict[key] = value.strip('\r')
        
        return data_dict

    request = str(request)
#     print(request)
    if "POST" in request:
        headers, post_data = request.split('\r\n\r\n', 1)
        print('- Headers:\n', headers)
        print('- Data:\n', post_data)
        headers_dict = text_to_dict(headers) # :dict
        print('headers_dict: ', headers_dict)
        
        if post_data != '':
            try:
                post_data = json.loads(post_data.strip(' '))
                print(post_data, '<-- post_data')
                if 'login' in post_data.keys() and 'password' in post_data.keys():
                    print(post_data['login'], '<-- login')
                    print(post_data['password'], '<-- password')
            except:
                post_data = None
                print('Have not wifi_data')
            finally:
                return headers_dict, post_data
    
    return headers_dict, None
