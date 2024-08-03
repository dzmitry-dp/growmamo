from network import WLAN, AP_IF, STA_IF, AUTH_WPA2_PSK

def setup_ssid():
    "Функция для настройки точки доступа"
    SSID = 'for_MAMO_app'
    PASSWORD = 'GrowMamo'

    my_ssid = WLAN(AP_IF) # объект для точки доступа
    my_ssid.active(True)  # активировать точку доступа
    my_ssid.config(ssid=SSID, key=PASSWORD, security=AUTH_WPA2_PSK) # изменить имя для точки доступа
    my_ssid.ifconfig(('192.168.1.1', '255.255.255.0', '192.168.2.1', '8.8.8.8')) # изменить ip, маску, шлюз и DNS-сервер (ip, subnet, gateway, dns)

    return my_ssid

def connect_to_home_wifi(login, password):
    "Подключение к домашнему роутеру"
    home_wifi = WLAN(STA_IF) # объект для подключения к роутеру
    home_wifi.active(True)
    print('Connecting to network...')
    home_wifi.connect(login, password) # login = SSID, password = key

    return home_wifi

def time_synchronization():
    "Получетение текущей даты и времени из сети интернет"
    import ntptime
    from machine import RTC
    
    try:
        rtc = RTC()
        ntptime.settime() # set the rtc datetime from the remote server
        print('Now : ', rtc.datetime())    # (year, month, day, weekday, hours, minutes, seconds, subseconds)
    except OSError:
        print('Не удалось синхронизировать время')
