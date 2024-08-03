############################################################
### Проверка на наличие сохраненного пароля от домашнего wifi
from memory import read_file, ujson

login, password = read_file('wifi_login')

from wifi import setup_ssid, connect_to_home_wifi, time_synchronization
import time

##########################################################################################
### В зависимости от наличия файлов создаем точку доступа или подключаемся к домашней сети
if login and password:
    home_wifi = connect_to_home_wifi(login, password)
    # Ожидаем подключение 10 секунд
    for _ in range(10):
        if home_wifi.isconnected():
            print('Подключено к сети', login)
            print('IP-адрес:', home_wifi.ifconfig()[0])
            
            time_synchronization() # сразу после подключения к сети синхронизируем время
        
            try: # пробуем отключить точку доступа
                mamo_ssid.active(False)
            except NameError:
                mamo_ssid = setup_ssid() # объект для точки доступа
                mamo_ssid.active(False)  # деактивировать точку доступа
            ###################
            ### Работаем с mqtt
            import mqtt_swap
            break
        print('.')
        time.sleep(1)
    else:
        print('Не удалось подключиться к домашней сети')
        mamo_ssid = setup_ssid() # создаем свою точку доступа с ssid for_MAMO_app
        home_wifi.active(False) # бросаем попытки подключиться к роутеру
            
else: # если нет пароля к домашнему wifi
    mamo_ssid = setup_ssid() # создаем свою точку доступа с ssid for_MAMO_app

####################################
### Настраиваем информационные пины
import machine

led = machine.Pin(2, machine.Pin.OUT, value = 0) # Настройка встроенного светодиода на ESP8266

pin_a = machine.Pin(14, machine.Pin.OUT, value = 0) # информационный pin
pin_b = machine.Pin(12, machine.Pin.OUT, value = 0) # информационный pin
pin_c = machine.Pin(13, machine.Pin.OUT, value = 0) # информационный pin
pin_d = machine.Pin(15, machine.Pin.OUT, value = 0) # pin управления

# pin_d(1) # включил запись в регистр
# pin_a(1) # выставил 1 на пине D5
# pin_b(1) # выставил 1 на пине D6
# pin_c(1) # выставил 1 на пине D7
# pin_d(0) # даю разрешение на чтение состояния pin_a, pin_b, pin_c   

###############################################################
### Настраиваем сокеты для работы с точкой доступа for_MAMO_app
import access_point

access_point.start(mamo_ssid, login, password) # mamo_ssid - объект управления точкой доступа, login - ssid точки доступа домашнего wifi, password - пароль от домашнего wifi
