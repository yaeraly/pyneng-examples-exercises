# -*- coding: utf-8 -*-
import re
from pprint import pprint
'''
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них (второй).

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким образом, чтобы она возвращала список кортежей для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет несколько кортежей.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''
def get_ip_from_cfg(filename):
    regex = ('interface (?P<intf>\S+)'
             '| +\S+ +\S+ +(?P<ip2>\d+\.\d+\.\d+\.\d+) (?P<mask2>\d+\.\d+\.\d+\.\d+) secondary'
             '| +\S+ +\S+ +(?P<ip1>\d+\.\d+\.\d+\.\d+) (?P<mask1>\d+\.\d+\.\d+\.\d+)')

    ip_dict = {}
    with open(filename) as f:
        for line in f:
            match = re.search(regex, line)
            if match:
                if match.lastgroup == 'intf':
                    intf = match.group(match.lastgroup)
                elif match.lastgroup == 'mask1':
                    ip_dict[intf] = []
                    ip_dict[intf].append(match.group('ip1', 'mask1'))
                else:
                    ip_dict[intf].append(match.group('ip2', 'mask2'))
    return ip_dict

pprint(get_ip_from_cfg('config_r2.txt'))


