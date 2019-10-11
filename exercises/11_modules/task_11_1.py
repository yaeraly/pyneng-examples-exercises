# -*- coding: utf-8 -*-
from pprint import pprint
'''
Задание 11.1

Создать функцию parse_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

У функции должен быть один параметр command_output, который ожидает как аргумент вывод команды одной строкой (не имя файла). Для этого надо считать все содержимое файла в строку.

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}

В словаре интерфейсы должны быть записаны без пробела между типом и именем. То есть так Fa0/0, а не так Fa 0/0.

Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

def parse_cdp_neighbors(command_output):
    result_dict = {}

    for line in command_output.split('\n'):

        if '>' in line:
            l_device = line.split('>')[0]
        elif '/' in line:
            r_device, l_intf_t, l_intf_n, *others, r_intf_t, r_intf_n = line.split()
            result_dict[(l_device, l_intf_t + l_intf_n)] = (r_device, r_intf_t + r_intf_n)

    return result_dict

if __name__ == "__main__":
    with open("sh_cdp_n_sw1.txt") as f:
        pprint(parse_cdp_neighbors(f.read()))

