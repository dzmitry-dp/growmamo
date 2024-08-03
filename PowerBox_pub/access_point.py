import gc
import ujson
import select
import machine

from web import ports, create_sockets, web_data, handle_post_request


def start(mamo_ssid, login, password):
    sockets = create_sockets(mamo_ssid = mamo_ssid)

    try:
        while True:
            readable, _, _ = select.select(list(sockets.keys()), [], [])
            
            for sock in readable:
                try:
                    gc.collect()

                    conn, addr = sock.accept()
                    port = sockets[sock]  # Получаем порт из словаря
                    conn.settimeout(1.0)
                    print('Received HTTP GET connection request from %s' % str(addr))
                    
                    request = conn.recv(1024)
                    print('request: ', request)

                    if request:
                        request = request.decode()
                    else:
                        break
                        
                    if port == ports[0]: # если 80 потр
                        conn.settimeout(None)
                        response = web_data()
                        conn.sendall(response)
                        print('response: ', response)
                        conn.close()
                        
                    elif port == ports[1]: # 5678 порт для управления
                        conn.settimeout(None)
                        headers_dict, post_data = handle_post_request(request)
                        
                        if headers_dict['User-Agent'] == 'MAMO_app': # Если в заголовке данных User-Agent: MAMO_app, то продолжаем обработку
                            if not login and not password: # если нет данных login и password в файле wifi_login
                                try:
                                    if post_data: # если есть специальные данные в post запросе
                                        if 'login' in post_data.keys() and 'password' in post_data.keys():
                                            print('--- Запись login и password в файл wifi_login')
                                            with open('wifi_login', "w") as file:
                                                ujson.dump(post_data, file)
                                            machine.reset() # Перезагрузка устройства если небыло login и пароля в файле
                                except KeyError:
                                    pass # нет данных о wifi_login в POST сообщении клиента
                            else: # если в файле записан login и password
                                try:
                                    if post_data: # если есть специальные данные в post запросе
                                        if 'login' in post_data.keys() and 'password' in post_data.keys():
                                            if post_data['login'] != login or post_data['password'] != password:
                                                print('Новые данные login или password')
                                                print('--- Запись login и password в файл wifi_login')
                                                with open('wifi_login', "w") as file:
                                                    ujson.dump(post_data, file)
                                                machine.reset() # Перезагрузка устройства если небыло login и пароля в файле
                                except KeyError:
                                    pass # нет данных о wifi_login в POST сообщении клиента
                except OSError:
                    conn.close()
                finally:
                    conn.close()

    except KeyboardInterrupt:
        print('Server is shutting down...')
    finally:
        for sock in sockets:
            sock.close()
        print('Correct Finally')
