# -*- coding: utf-8 -*-
import yaml
from netmiko import ConnectHandler, NetMikoAuthenticationException
from concurrent.futures import ThreadPoolExecutor
'''
Задание 20.3

Создать функцию send_command_to_devices, которая отправляет
разные команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
'''

commands = {'192.168.100.1': 'sh ip int br',
            '192.168.100.2': 'sh arp',
            '192.168.100.3': 'sh ip int br'}


def send_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = f'{ssh.find_prompt()}{command}\n{ssh.send_command(command)}'

            return result
    except(NetMikoAuthenticationException) as err:
        print("Invalid username or password")


def send_command_to_devices(devices, commands_dict, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(send_command, devices, commands_dict.values())

    with open(filename, 'w') as dst:
        dst.write('\n'.join(results))

if __name__ in "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)

    send_command_to_devices(devices, commands, 'task_20_2.txt')
