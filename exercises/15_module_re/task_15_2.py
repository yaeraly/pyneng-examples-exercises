# -*- coding: utf-8 -*-
import re
from pprint import pprint
'''
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

'''
def parse_sh_ip_int_br(filename):
    regex = re.compile('(?P<intf>\S+) +(?P<ip>\S+) +\S+ +\S+ +(?P<status>up|\S+ \S+) +(?P<protocol>up|down)')
    conf_list = []
    with open(filename) as f:
        for line in f:
            match = regex.search(line)
            if match:
                conf_list.append(match.groups())
    return conf_list

if __name__ == '__main__':
    pprint(parse_sh_ip_int_br('sh_ip_int_br.txt'))

