# -*- coding: utf-8 -*-
'''
Задание 6.1

Список mac содержит MAC-адреса в формате XXXX:XXXX:XXXX.
Однако, в оборудовании cisco MAC-адреса используются в формате XXXX.XXXX.XXXX.

Создать скрипт, который преобразует MAC-адреса в формат cisco
и добавляет их в новый список mac_cisco

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

mac = ['aabb:cc80:7000', 'aabb:dd80:7340', 'aabb:ee80:7000', 'aabb:ff80:7000']

mac_cisco = [ m.replace(':', '.') for m in mac ]
print(mac_cisco)

mac_c = []
i = 0
while len(mac) != i :
    mac_c.append(mac[i].replace(':', '.'))
    i += 1
print(mac_c)

