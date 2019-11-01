# -*- coding: utf-8 -*-
import yaml
from netmiko import ConnectHandler
'''
Задание 19.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к одному устройству и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml с помощью функции send_show_command.

'''

command = 'sh ip int br'

def send_show_command(device, command):
    result = ''
    with ConnectHandler(**device) as ssh:
        ssh.enable()

        result = ssh.send_command(command)

    return result

if __name__ in "__main__":
    with open('devices.yaml') as f:
        dict_device = yaml.safe_load(f)
        print(send_show_command(dict_device[0], command))
