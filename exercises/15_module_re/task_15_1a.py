# -*- coding: utf-8 -*-
import re
from pprint import pprint
'''
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом, чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1':('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2':('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''

def get_ip_from_cfg(filename):
    regex = re.compile(r'interface (?P<intf>\S+)'
                       r'| +\S+ +\S+ +(?P<ip>\d+\.\d+\.\d+\.\d+) (?P<mask>\d+\.\d+\.\d+\.\d+)')

    ip_dict = {}
    with open(filename) as f:
        for line in f:
            match = regex.search(line)
            if match:
                if match.lastgroup == 'intf':
                    intf = match.group(match.lastgroup)
                else:
                    ip_dict[intf] = match.group('ip', 'mask')

    return ip_dict

pprint(get_ip_from_cfg('config_r1.txt'))

