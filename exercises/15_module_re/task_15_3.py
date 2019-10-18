# -*- coding: utf-8 -*-
import re
from pprint import pprint
'''
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
'''

asa_config = """
object network LOCAL_{0}
 host {0}
 nat (inside,outside) static interface service tcp {1} {2}
"""

def convert_ios_nat_to_asa(src_filename, dest_filename):
    regex = re.compile('.+tcp (?P<ip>\d+\.\d+\.\d+\.\d+) (?P<port1>\d+) \S+ \S+ (?P<port2>\d+)')
    asa_list = []
    with open(src_filename) as src, open(dest_filename, 'w') as dest:
        for l in src:
            line = l.strip()
            match = regex.search(line)
            p1 = match.group("port1")
            p2 = match.group("port2")
            asa_list.append(f"object network LOCAL_{match.group('ip')}\n")
            asa_list.append(f' host {match.group("ip")}\n')
            asa_list.append(f' nat (inside,outside) static interface service tcp {p1} {p2}\n')

        dest.writelines(asa_list)

convert_ios_nat_to_asa('cisco_nat_config.txt', 'cisco_asa_config.txt')

