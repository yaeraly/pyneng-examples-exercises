# -*- coding: utf-8 -*-
import subprocess
from concurrent.futures import ThreadPoolExecutor

'''
Задание 20.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.
'''
ip_addresses = ['192.168.100.1', '192.168.100.2', '192.168.100.4']


def ping_ip(ip_address):
    reply = subprocess.run(['ping', '-c', '1', '-n', f'{ip_address}'],
                           stdout=subprocess.DEVNULL)

    if reply.returncode == 0:
        return True
    else:
        return False


def ping_ip_addresses(ip_list, limit=3):
    reach_ip = []
    unreach_ip = []

    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(ping_ip, ip_list)
        for ip, reply in zip(ip_list, results):
            if reply is True:
                reach_ip.append(ip)
            else:
                unreach_ip.append(ip)

    return (reach_ip, unreach_ip)

print(ping_ip_addresses(ip_addresses))

