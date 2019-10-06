# -*- coding: utf-8 -*-
'''
Задание 6.2

1. Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
2. Определить тип IP-адреса.
3. В зависимости от типа адреса, вывести на стандартный поток вывода:
   'unicast' - если первый байт в диапазоне 1-223
   'multicast' - если первый байт в диапазоне 224-239
   'local broadcast' - если IP-адрес равен 255.255.255.255
   'unassigned' - если IP-адрес равен 0.0.0.0
   'unused' - во всех остальных случаях


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''
ip_address = input('Enter IP address in a format (10.10.10.1): ')
ip = int(ip_address.split('.')[0])

if 1 <= ip <= 223:
    print(f"\nThe {ip_address} is an unicast")
elif 224 <= ip <= 239:
    print(f"\nThe {ip_address} is a multicast")
elif ip_address == '255.255.255.255':
    print(f"\nThe {ip_address} is a local broadcast")
elif ip_address == '0.0.0.0':
    print(f"\nThe {ip_address} is an unassigned")
else:
    print(f"\nThe {ip_address} is an unused")

