# -*- coding: utf-8 -*-
import yaml
from itertools import repeat
from netmiko import ConnectHandler, NetMikoAuthenticationException
from concurrent.futures import ThreadPoolExecutor

'''
Задание 20.2

Создать функцию send_show_command_to_devices, которая отправляет
одну и ту же команду show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
'''


def send_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = f'{ssh.find_prompt()}{command}\n{ssh.send_command(command)}'

            return result
    except(NetMikoAuthenticationException) as err:
        print("Invalid username or password")


def send_show_command_to_devices(devices, command, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(send_command, devices, repeat(command))

    with open(filename, 'w') as dst:
        dst.write('\n'.join(results))

if __name__ in "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)

    send_show_command_to_devices(devices, 'sh ip int br', 'task_20_2.txt')

