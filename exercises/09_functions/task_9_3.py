# -*- coding: utf-8 -*-
'''
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

def get_int_vlan_map(config_filename):
    access_intf = {}
    trunk_intf = {}
    with open(config_filename) as f:
        for line in f:
            if line.startswith('interface'):
                intf = line.split()[-1]
            elif 'access vlan' in line:
                vlan = int(line.split()[-1])
                access_intf[intf] = vlan
            elif 'allowed vlan' in line:
                vlans = line.split()[-1].split(',')
                trunk_intf[intf] = [ int(num) for num in vlans ]

    return_tuple = (access_intf, trunk_intf)
    return return_tuple

print(get_int_vlan_map('config_sw1.txt'))

