# -*- coding: utf-8 -*-
import yaml
from netmiko import ConnectHandler, NetMikoAuthenticationException
from concurrent.futures import ThreadPoolExecutor

'''
Задание 20.3a

Создать функцию send_command_to_devices, которая отправляет
список указанных команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какие команды. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом каждой команды надо написать имя хоста и саму команду):

R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          87   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R1#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.30.0.1               -   aabb.cc00.6530  ARPA   Ethernet0/3.300
Internet  10.100.0.1              -   aabb.cc00.6530  ARPA   Ethernet0/3.100
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down
R3#sh ip route | ex -

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
O        10.1.1.1/32 [110/11] via 192.168.100.1, 07:12:03, Ethernet0/0
O        10.30.0.0/24 [110/20] via 192.168.100.1, 07:12:03, Ethernet0/0


Порядок команд в файле может быть любым.

Для выполнения задания можно создавать любые дополнительные функции, а также использовать функции созданные в предыдущих заданиях.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
'''

commands = {'192.168.100.1': ['sh ip int br', 'sh arp'],
            '192.168.100.2': ['sh arp'],
            '192.168.100.3': ['sh ip int br', 'sh ip route | ex -']}


def send_command(device, commands):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ''
            for com in commands:
                result += f'{ssh.find_prompt()}{com}\n{ssh.send_command(com)}\n'

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

