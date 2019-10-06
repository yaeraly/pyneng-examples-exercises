# -*- coding: utf-8 -*-
'''
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса. Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой,
   - каждое число в диапазоне от 0 до 255.

Если адрес задан неправильно, выводить сообщение:
'Неправильный IP-адрес'

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ip_address = input('Enter IP address in a format (10.10.10.1): ')

try:
    ip = [ int(i) for i in ip_address.split('.') ]

    if len(ip) == 4:
        for i in ip:
            if 0 <= i <= 255:
                incorrect_ip = False
            else:
                incorrect_ip = True
                break

    if incorrect_ip == False:
        if 1 <= ip[0] <= 223:
            print(f"\nThe {ip_address} is an unicast")
        elif 224 <= ip[0] <= 239:
            print(f"\nThe {ip_address} is a multicast")
        elif ip_address == '255.255.255.255':
            print(f"\nThe {ip_address} is a local broadcast")
        elif ip_address == '0.0.0.0':
            print(f"\nThe {ip_address} is an unassigned")
        else:
            print(f"\nThe {ip_address} is an unused")

    else:
        print("Incorrect IP address")

except:
    print("Incorrect IP address")

