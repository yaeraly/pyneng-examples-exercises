# -*- coding: utf-8 -*-
import re
from pprint import pprint
'''
Задание 17.2

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
'''
#SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1
def parse_sh_cdp_neighbors(file_content):
    regex = re.compile(r'(?P<l_device>\S+)[>#]'
                       r'|(?P<r_device>\S+) +(?P<l_intf>\S+ \S+) +\d+.+\S+ +(?P<r_intf>\S+ \S+)')
    result_dict = {}
    for line in file_content.split('\n'):
        match = regex.search(line)
        if match and match.lastgroup == 'l_device':
            l_dev = match.group('l_device')
            result_dict[l_dev] = {}
        elif match:
            result_dict[l_dev][match.group('l_intf')] = {}
            result_dict[l_dev][match.group('l_intf')][match.group('r_device')] = {}
            result_dict[l_dev][match.group('l_intf')][match.group('r_device')] = match.group('r_intf')

    return result_dict

if __name__ in '__main__':
    with open('sh_cdp_n_sw1.txt') as f:
        pprint(parse_sh_cdp_neighbors(f.read()))

