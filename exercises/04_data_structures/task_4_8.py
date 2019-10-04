# -*- coding: utf-8 -*-
'''
Задание 4.8

Преобразовать IP-адрес в двоичный формат и вывести на стандартный поток вывода вывод столбцами, таким образом:
- первой строкой должны идти десятичные значения байтов
- второй строкой двоичные значения

Вывод должен быть упорядочен также, как в примере:
- столбцами
- ширина столбца 10 символов

Пример вывода для адреса 10.1.1.1:
10        1         1         1
00001010  00000001  00000001  00000001

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ip = '192.168.3.1'
ip1, ip2, ip3, ip4 = ip.split('.')

show1 = f"""
{ip1:<8}  {ip2:<8}  {ip3:<8}  {ip4:<8}
{int(ip1):08b}  {int(ip2):08b}  {int(ip3):08b}  {int(ip4):08b}
"""
print(show1)

template = """
{0:<8}  {1:<8}  {2:<8}  {3:<8}
{0:08b}  {1:08b}  {2:08b}  {3:08b}
"""
show2 = template.format(int(ip1), int(ip2), int(ip3), int(ip4))
print(show2)

