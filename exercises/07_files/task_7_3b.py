# -*- coding: utf-8 -*-
'''
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Дополнить скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
VLAN = input(f'Enter vlan: ')

lists = []
with open('CAM_table.txt') as f:
    for line in f:
        if 'DYNAMIC' in line:
            vlan, mac, _, intf = line.split()
            if vlan == VLAN:
                lists.append([ int(vlan), mac, intf ])

lists.sort()
for vlan, mac, intf in lists:
    print(f'{vlan:<7}    {mac}   {intf:>7}')

